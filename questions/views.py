import json
import requests
from django.http import JsonResponse
from .models import Question
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process_post_request(request: json) -> JsonResponse:
    """
    Представление проверяет корректность post-запроса, вызывает функцию record_questions для записи новых вопросов
    в базу данных и возвращает json с информацией о последнем вопросе в базе данных на момент запроса, либо же пустой
    объект, если записей не было.
    :param request: json с параметрами {'questions_num': int}
    :return: JsonResponse
    """
    if request.method == "POST":
        if 'questions_num' not in request.POST:
            return JsonResponse({'error': 'Required query parameter for questions_num is missing'}, status=400)
        questions_num = request.POST.get('questions_num')
        if not questions_num.isnumeric():
            return JsonResponse({'error': 'Parameter questions_num should be non-negative integer'}, status=400)
        questions_num = int(questions_num)
        previous_question = Question.objects.order_by('-created_at').first()
        record_result = record_questions(questions_num)
        if record_result == 'Bad result':
            return JsonResponse({'message': 'Can not add unique questions to database'}, status=500)
        if previous_question:
            return JsonResponse({'id': previous_question.pk,
                                 'initial_id': previous_question.initial_id,
                                 'question': f'{previous_question.text}',
                                 'answer': f'{previous_question.answer}',
                                 'original_date': f'{previous_question.original_date}',
                                 'created_at': f'{previous_question.created_at}'
                                 }, status=200)
        return JsonResponse({}, status=200)

    elif request.method == "GET":
        return JsonResponse({"message": "Send post-request in json-format: {'questions_num': integer}"
                                        " where integer >= 0"}, status=200)


def record_questions(questions_num: int) -> str:
    """
    Функция получает число новых вопросов, которые нужно записать в базу данных. На сайт с вопросами отправляется
    get-запрос на получение соответствующего количества новых вопросов. Если были получены уже записанные в базу данных
    вопросы, то отправляются новые запросы, пока не будет получено требуемое количество вопросов. После 100 неудачных
    попыток запросы прекращаются.
    :param questions_num: число вопросов, которые нужно записать в базу данных.
    :return: 'Good result' или 'Bad result'
    """
    r = requests.get(f'https://jservice.io/api/random?count={questions_num}')
    items = json.loads(r.content)
    for item in items:
        initial_id = item['id']
        if Question.objects.filter(initial_id=initial_id).exists():
            continue
        question = item["question"]
        answer = item['answer']
        original_date = item['created_at']
        new_question = Question(initial_id=initial_id, text=question, answer=answer, original_date=original_date)
        new_question.save()
        questions_num -= 1

    # Если были повторы вопросов, то делаем 100 попыток получить новые
    tries = 0
    while questions_num:
        # берём с запасом, чтобы делать меньше запросов
        r = requests.get(f'https://jservice.io/api/random?count={questions_num * 5}')
        items = json.loads(r.content)
        for item in items:
            initial_id = item['id']
            if Question.objects.filter(initial_id=initial_id).exists():
                continue
            question = item["question"]
            answer = item['answer']
            original_date = item['created_at']
            new_question = Question(initial_id=initial_id, text=question, answer=answer, original_date=original_date)
            new_question.save()
            questions_num -= 1
            if not questions_num:
                break
        tries += 1
        if tries == 100:
            return 'Bad result'
    return 'Good result'

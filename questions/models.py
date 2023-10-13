from django.db import models


class Question(models.Model):
    '''
    Поля модели:
    initial_id - идентификатор вопроса на сайте с вопросами;
    text - текст вопроса;
    answer - ответ на вопрос;
    original_date - дата создания вопроса на сайте с вопросами;
    created_at - дата создания записи в базе данных;
    '''
    initial_id = models.IntegerField(default=0, verbose_name='ID вопроса')
    text = models.TextField(verbose_name='Вопрос')
    answer = models.CharField(max_length=255, verbose_name='Ответ')
    original_date = models.DateTimeField(verbose_name='Первоначальная дата')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self) -> str:
        return f'{self.initial_id} {self.text} {self.answer}, {self.original_date}, {self.created_at}'

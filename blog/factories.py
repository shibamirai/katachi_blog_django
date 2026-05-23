import factory
from customauth.models import CustomUser
from factory.faker import faker
from .models import Post, Category


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        django_get_or_create = ('email',)   # 同じemailのユーザーが存在すれば取得、

    name = factory.Faker('name', locale='ja')
    email = factory.Faker('ascii_email')
    password = factory.PostGenerationMethodCall('set_password', 'password') # パスワードは'password'


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    
    slug = factory.Faker('slug')
    title = factory.Faker('text', locale='ja', max_nb_chars=20)
    author = factory.Faker('random_element', elements=list(CustomUser.objects.filter(is_admin=1)))
    category = factory.Faker('random_element', elements=list(Category.objects.all()))
    posted_at = factory.Faker('date_between')

    @factory.lazy_attribute
    def body(self):
        """
        body を複数段落の文章にする
        """
        paragraphs = ""
        for _ in range(0, 5):
            paragraphs += faker.Faker(locale='ja').paragraph(nb_sentences=10) + "\n\n"
        return paragraphs
        
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        posted_at の auto_now_add をオーバーライドして、上記のダミーの日付をセットする
        """
        posted_at = kwargs.pop("posted_at", None)
        obj = super()._create(model_class, *args, **kwargs)
        if posted_at is not None:
            model_class.objects.filter(id=obj.id).update(posted_at=posted_at)
        return obj
        
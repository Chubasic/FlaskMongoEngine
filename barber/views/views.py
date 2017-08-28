
from models.models import Post, Comment
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView, View
from flask_mongoengine.wtf import model_form


hello = Blueprint('hello', __name__, template_folder='templates')
posts = Blueprint('posts', __name__, template_folder='templates')
portfolio = Blueprint('portfolio', __name__, template_folder='templates')
about = Blueprint('about', __name__, template_folder='templates')
contact = Blueprint('contact', __name__, template_folder='templates')


class ListView(MethodView):

    def get(self, page=1):
        posts = Post.objects.paginate(page=page, per_page=3)
        return render_template('posts/list.html', posts=posts, page=page)

class DetailView(MethodView):

    form = model_form(Comment, exclude=['created_at'])

    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "post": post,
            "form": form
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('posts.detail', slug=slug))
        return render_template('posts/detail.html', **context)


class RenderTemplate(View):
    def __init__(self, template_name):
        self.template_name = template_name
    def dispatch_request(self):
        return render_template(self.template_name)





# Register the urls
hello.add_url_rule('/',view_func=RenderTemplate.as_view('hello', template_name='hello.html'))
posts.add_url_rule('/home/<int:page>', endpoint='/home/1',  view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
about.add_url_rule('/about', view_func=RenderTemplate.as_view('about', template_name='about.html'))
portfolio.add_url_rule('/portfolio', view_func=RenderTemplate.as_view('portfolio', template_name='portfolio.html'))
contact.add_url_rule('/contact/', view_func=RenderTemplate.as_view('contact', template_name='contact.html'))

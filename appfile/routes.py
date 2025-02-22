from flask import render_template , url_for , flash , redirect \
    , Blueprint , session , request , abort
from appfile.forms import ContactForm , BlogForm , IdentifyForm
from  flask_mail import   Message
from appfile.models import USER , POST
from appfile import db, mail 
from appfile.utils import get_project_titles
from flask import current_app

projects_names = get_project_titles()

routes_main = Blueprint('routes_main',__name__)


@routes_main.before_request
def reset_authenticated():
    if 'authenticated' not in session:
        session['authenticated'] = False
        session.modified = True

#add things in this route
@routes_main.route('/')
@routes_main.route('/home')
def home():
    return render_template('home.html',title="Home Page")

@routes_main.route('/about')
def about():
    return render_template('about.html')

@routes_main.route('/projects')
def projects():
    return render_template('projects_page.html' ,title='Projects', projects_names=projects_names)


@routes_main.route('/projects/<string:project_name>',methods=['GET'])
def project_detail(project_name):
    project_name = project_name.replace(' ','_').lower()

    if project_name not in [name.replace(' ','_').lower() for name in projects_names]:
        return render_template('errors/error404.html') , 404
    else:
        return render_template(f'projects/{project_name}.html',title=f'{project_name}',project_name=project_name)




@routes_main.route('/blog')
def blog():
    '''this function puts the blog posts that the admin created'''
    page = request.args.get('page',1,type=int)
    posts = POST.query.order_by(POST.date_posted.desc()).paginate(per_page=6,page=page)
    return render_template('blog.html',title='Blog',posts=posts)



@routes_main.route('/blog/identify' , methods = ['GET','POST'])
def identify():
    '''if authentication is not correct 
    it redirects him to an error page (403) otherwise it makes the admin to redirect
    to the url for creating a blog
    '''
    form = IdentifyForm()
    if form.validate_on_submit():    
        if form.email.data == 'admin@gmail.com' and form.password.data == 'admin12345':
            session['authenticated'] = True
            flash("You can continue",'success')
            return redirect(url_for('routes_main.blog_new'))
        else:
            session['authenticated'] = False
            return render_template('errors/error403.html') , 403
    elif request.method == 'GET':
        return render_template('login.html',form=form,legend='Authenticate')
    

@routes_main.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = POST.query.get_or_404(post_id)
    return render_template('blog_id.html',title=post.title,post=post)



@routes_main.route('/blog/<int:post_id>/update',methods=['GET','POST'])
def update_blog(post_id):

    update_post = POST.query.get_or_404(post_id)
    if not session.get('authenticated'):
        abort(403)
    
    form = BlogForm()
    if form.validate_on_submit():
        update_post.title = form.title.data
        update_post.content = form.content.data
        db.session.commit()
        flash("Post has been updated",'success')
        return redirect(url_for('routes_main.blog_post',post_id = update_post.id))
    elif request.method == "GET":
        form.title.data = update_post.title
        form.content.data = update_post.content 
    
    return render_template('blog_create.html',title="Update Post",legend="Update Post", form=form)


@routes_main.route('/blog/delete/<int:post_id>',methods=['GET','POST'])
def delete_blog(post_id):
    post = POST.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted",'success')
    return redirect(url_for('routes_main.blog',title="My Blog"))



@routes_main.route('/blog/create',methods=['GET','POST'])
@routes_main.route('/blog/new',methods = ['GET','POST'])
@routes_main.route('/blog/new_post',methods = ['GET','POST'])
def blog_new():
    '''
    if admin is authenticated correctly then we can go to this route so he can create a blog post
    '''
    print(f"DEBUG: Session authenticated -> {session.get('authenticated')}")
    #it checks if the admin has been authenticated so he can create a post for him
    
    if not session.get('authenticated'):
        flash("You must authenticate first that you are the owner",'danger')
        return redirect(url_for('routes_main.identify')) #if not then it returns a message and it makes him go to the identify page
    
   
    form = BlogForm()
    if form.validate_on_submit():
      print(form)
      post = POST(title = form.title.data , content = form.content.data)
      db.session.add(post)
      db.session.commit()
      print(f"DEBUG: New post -> {post}")
      flash('The post was created ','success')
      return redirect(url_for('routes_main.blog'))
              
    return render_template('blog_create.html',form =form ,legend = "Create Post" , title ="New Post Page")




'''the errors is for the app if we have any problem to solve it using the below functions '''

@routes_main.app_errorhandler(404)
def error_404(error):
    return render_template('errors/error404.html'),404

@routes_main.app_errorhandler(403)
def error_403(error):
    return render_template('errors/error403.html'),403

@routes_main.app_errorhandler(500)
def error_500(error):
    return render_template('errors/error500.html'),500





@routes_main.route('/contact',methods=['GET','POST'])
def contact():
    """
    it sends to my email the information of the person that wants to contact with me 
    """

    form = ContactForm()
    if form.validate_on_submit():
        
        name = form.name.data    
        email = form.email.data
        text_area = form.text_area.data
        user = USER(name = form.name.data , email = form.email.data , text_area= form.text_area.data)
        db.session.add(user)
        db.session.commit()
        msg = Message("New Message from" + name, recipients=['d.zoumpos04@gmail.com'])
        msg.body= f"Name: {name},\nEmail: {email},\nMessage: {text_area}"
        try:
            mail.send(msg)
            flash("Thanks for submiting i will contact you soon",'success')
        except Exception as e:
            flash("Something went wrong while trying to send the message",'danger')
        return redirect(url_for('routes_main.home'))
           
    return render_template('contact.html',form=form , title="Contact Page")


from django.shortcuts import render
from .models import Post, Contact, Comments
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from imblearn.over_sampling import SMOTE, BorderlineSMOTE, ADASYN
from scipy.stats import zscore
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, PolynomialFeatures
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier


def about(request):
    return render(request, 'blogs/about.html', {'title':"About Page"})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        content = request.POST.get('content')

        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been received")

    return render(request, 'blogs/contact.html', {'title': "Contact Page"})

def test(request):
    return render(request, 'blogs/test.html', {'title': "Testing Page"})

def explore(request):
    return render(request,'blogs/explore.html', {'title':"Explore More"} )

def meds(request):
    return render(request, 'blogs/meds.html', {'title':"Medications"})

def consult(request):
    return render(request, 'blogs/doctorpage.html', {'title':"Consult" })

def exercises(request):
    return render(request, 'blogs/exercise.html', {'title':"Yoga" })


def pretest(request):
    return render(request,'blogs/pre_test.html', {'title':"Pre Test"} )

#def result(request):
    #data= pd.read_csv(r"C:\Users\espar\Downloads\diabetes.csv")
    #X = data.drop("Outcome", axis=1) 
    #Y = data["Outcome"]
    #X_train, X_test, Y_train, Y_test= train_test_split(X,Y, test_size=0.2)
    #model= LogisticRegression(max_iter=500)
    #model.fit(X_train, Y_train)
    #val1= float(request.GET['n1'])
    #val2= float(request.GET['n2'])
    #val3= float(request.GET['n3'])
    #val4= float(request.GET['n4'])
    #val5= float(request.GET['n5'])
    #val6= float(request.GET['n6'])
    #val7= float(request.GET['n7'])
    #val8= float(request.GET['n8'])
    #pred= model.predict([[val1, val2,val3,val4,val5,val6,val7,val8]])
    #result2=""
    #if pred==[1]:
     #   result2="Positive"
    #else:
    #    result2="Negative"
    #return render(request, "blogs/test.html", {"result2": result2})
import pandas as pd
import joblib
from django.shortcuts import render
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

# Initialize model and scaler once
try:
    model = joblib.load('diabetes_model.pkl')
    scaler = joblib.load('diabetes_scaler.pkl')
    feature_columns = joblib.load('feature_columns.pkl')
except:
    model = scaler = feature_columns = None

def train_and_save_model():
    # Load and preprocess data
    df = pd.read_csv(r"C:\Users\Acer\Downloads\diabetes_prediction_dataset.csv")
    
    # Clean data
    df = df[df['age'] > 0]  # Remove invalid ages
    
    # Feature engineering
    df['smoking_history'] = df['smoking_history'].str.lower().str.replace(' ', '_')
    df = pd.get_dummies(df, columns=['gender', 'smoking_history'])
    
    # Split data
    X = df.drop('diabetes', axis=1)
    y = df['diabetes']
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Handle class imbalance
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X_train, y_train)
    
    # Train model
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_res)
    
    svm = SVC(kernel='rbf', C=1.5, class_weight='balanced', probability=True)
    svm.fit(X_scaled, y_res)
    
    # Save artifacts
    joblib.dump(svm, 'diabetes_model.pkl')
    joblib.dump(scaler, 'diabetes_scaler.pkl')
    joblib.dump(X.columns.tolist(), 'feature_columns.pkl')

def result(request):
    if not model:
        train_and_save_model()
        
    if request.method == 'POST':
        try:
            # Prepare input DataFrame with the same columns as training data
            user_data = pd.DataFrame(columns=feature_columns).fillna(0)  # Fill NaN values with 0
            
            # Numerical features
            user_data['age'] = [max(0.1, float(request.POST['n2']))]  # Handle infant ages
            user_data['bmi'] = [float(request.POST['n6'])]
            user_data['HbA1c_level'] = [float(request.POST['n7'])]
            user_data['blood_glucose_level'] = [float(request.POST['n8'])]
            user_data['hypertension'] = [int(request.POST['n3'])]
            user_data['heart_disease'] = [int(request.POST['n4'])]
            
            # Categorical features
            gender = request.POST['n1'].lower()
            smoking = request.POST['n5'].lower().replace(' ', '_')
            
            gender_col = f"gender_{gender}"
            smoking_col = f"smoking_history_{smoking}"
            
            if gender_col in user_data.columns:
                user_data[gender_col] = 1
            if smoking_col in user_data.columns:
                user_data[smoking_col] = 1

            # Handle any remaining missing values (in case they exist after filling)
            user_data = user_data.fillna(0)  # Replace missing values with 0 (or any other default)

            # Scale the data and predict
            scaled_data = scaler.transform(user_data)
            proba = model.predict_proba(scaled_data)[0][1]  # Get positive class probability
            result = "Positive" if proba > 0.35 else "Negative"  # Adjusted threshold
            
            return render(request, "blogs/test.html", {
                "result": result,
                "confidence": f"{proba*100:.1f}%"
            })
            
        except Exception as e:
            return render(request, "blogs/test.html", {"error": f"Error: {str(e)}"})
    
    return render(request, "blogs/test.html")



class PostListView(LoginRequiredMixin, ListView):
    model=Post
    template_name='blogs/home.html'
    context_object_name='posts'
    ordering=["-date_created"]


class PostDetailView(LoginRequiredMixin, DetailView):
    model=Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model= Post
    fields=['title', 'content']

    def form_valid(self, form):
        form.instance.author= self.request.user
        return super().form_valid(form)
    
    
    

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model=Post
    fields=['title', 'content']

    def form_valid(self, form):
        form.instance.author= self.request.user
        return super().form_valid(form)
    
    
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    
    

class PostDeleteView(DeleteView):
    model=Post
    success_url= '/'

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    

class CommentCreateView(LoginRequiredMixin,CreateView):
    model=Comments
    fields=('comment',)
    template_name='blogs/comment.html'
    success_url= reverse_lazy('bloghome')


    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)












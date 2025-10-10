from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
import spacy
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required

nlp = spacy.load("en_core_web_sm")

def home_view(request):
	return render(request,'home.html')

def about_view(request):
	return render(request,'about.html')

def contact_view(request):
	return render(request,'contact.html')

@login_required(login_url="login")
def animation_view(request):
	if request.method == 'POST':
		text = request.POST.get('sen')
		# Tokenizing the sentence
		text = text.lower()
		words = [token.text for token in nlp(text) if not token.is_space]

		tagged = [(token.text, token.tag_) for token in nlp(text)]
		
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])

		# Stopwords set
		stop_words = set(["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])

		filtered_text = [w for w in words if w not in stop_words]

		# Adding the specific word to specify tense
		probable_tense = max(tense, key=tense.get)

		if probable_tense == "past" and tense["past"] >= 1:
			filtered_text.insert(0, "Before")
		elif probable_tense == "future" and tense["future"] >= 1:
			if "Will" not in filtered_text:
				filtered_text.insert(0, "Will")
		elif probable_tense == "present" and tense["present_continuous"] >= 1:
			filtered_text.insert(0, "Now")

		final_text = []
		for w in filtered_text:
			path = w + ".mp4"
			f = finders.find(path)
			if not f:
				for c in w:
					final_text.append(c)
			else:
				final_text.append(w)

		return render(request,'animation.html',{'words': final_text, 'text': text})
	else:
		return render(request,'animation.html')


def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request,user)
			return redirect('animation')
	else:
		form = UserCreationForm()
	return render(request,'signup.html',{'form':form})

def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('animation')
	else:
		form = AuthenticationForm()
	return render(request,'login.html',{'form':form})

def logout_view(request):
	logout(request)
	return redirect("home")

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def process_speech(request):
    if request.method == "POST":
        data = json.loads(request.body)
        speech_text = data.get("speech_text", "")

        # Convert text to sign language representation (Modify this as per your logic)
        sign_language_output = convert_text_to_sign(speech_text)

        return JsonResponse({"sign_language": sign_language_output})

def convert_text_to_sign(text):
    # Simple placeholder function to convert text to sign language
    return f"Sign language translation for: {text}"

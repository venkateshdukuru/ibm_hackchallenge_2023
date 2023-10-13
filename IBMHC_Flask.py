#!/usr/bin/env python
# coding: utf-8

# In[6]:


from flask import Flask, request, render_template
import pickle


# In[8]:


app = Flask(__name__)
model = pickle.load(open('/Users/venkatesh/Downloads/IBM ML Certificate Materials/IBMHC/model.pkl', 'rb'))


# In[9]:


@app.route('/')
def home():
    return render_template('Home_Page.html')


# In[10]:


@app.route('/input',methods = ['POST'])
def pred():
    
    gender = request.form.get('gender')
    stream_12 = request.form.get('12_stream')
    stream_d = request.form.get('d_stream')
    spl = request.form.get('spl')
    workex = request.form.get('workex')
    
    marks_10 = request.form.get('10_marks')
    marks_12 = request.form.get('12_marks')
    marks_d = request.form.get('d_marks')
    marks_et = request.form.get('et_marks')
    marks_mba = request.form.get('mba_marks')
    
    input = [[int(gender), float(marks_10), float(marks_12), 
              int(stream_12),  float(marks_d), int(stream_d), int(workex),
              float(marks_et), int(spl), float(marks_mba)]]

    import requests

    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "sRtTk5DjfFT_GzzWJQ5-1KsqwW1WfJ2sCb3BLXWeZPyG"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY,"grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [  "gender", "ssc_p","hsc_p", "hsc_s", "degree_p", "degree_t","workex","etest_p","specialisation","mba_p"],
                                       "values": [int(gender), float(marks_10), float(marks_12),int(stream_12), float(marks_d), int(stream_d), int(workex), float(marks_et), int(spl), float(marks_mba)]}]}

    response_scoring = requests.post(
        'https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/50e5b045-33e0-404c-bf55-f9d547142798/predictions?version=2021-05-01',json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    op = response_scoring.json()
    
    op = model.predict(input)[0]
    
    
    if op == 1:
        result = "Congratulations!!! You are likely to land a good Placement!!! Good Luck for Placement Season"
        
        s1 = "Make sure you are thorough with your basics."
        s2 = "Get your Résumé reviewed"
        
    else:
        result = "You have to improve your skills and scores to land a Placement."
        
        if marks_mba<75:
             s1 = "In case you are still in college, you can try to improve your MBA grades."
        else:
             s1 = "Your MBA grades are good."
        
        if marks_et<75:
             s2 = "You can give another attempt of Etest and try to improve your scores."
        else:
             s2 = "Your grades look good. Brush up on your basics and review your Résumé."
                
        
    outputs = {
    'status': result,
    'suggestion1': s1,
    'suggestion2': s2
}
        
    return render_template('Home_Page.html', **outputs )


# In[13]:


if __name__ == '__main__':
    app.run()


# In[ ]:





from django.shortcuts import render,redirect
from .models import Trans,Cust
from django.http import HttpResponse
from datetime import datetime
from django.views.generic.base import View
from django.views.generic import TemplateView
from datetime import datetime
from django.core.mail import send_mail 
from django.conf import settings

def home(req):
 return render(req,'home.html',{})

def admin_portal(req):
 return render(req,'adminlog.html',{})

def login(req):
 custno=int(req.POST['custid'])
 pas=req.POST['passwd']
 try:
  obj=Cust.objects.get(custid=req.POST['custid'])
  if not(custno==obj.custid and pas==obj.passwd):
   obj=None
 except:
  obj=None
 if obj:
  print(obj.status)
  if 'log' in req.POST and custno!=101:
   if obj.status==1:
    return render(req,'custlog.html',{'user':obj})
   else:
    return render(req,'block.html',{})
  elif 'adminlog' in req.POST and custno==101:
    return render(req,'adminlog.html',{})
  else:
    return render(req,'home.html',{'incrt':2})
 else:
  return render(req,'home.html',{'incrt':2})
 
def newuser(req):
 last_record=Cust.objects.all().last()
 last_rec=(last_record.custid)+1
 return render(req,'newuser.html',{'custid':last_rec})

def edituser(req):
 return render(req,'edituser.html',{})

def blockuser(req):
 return render(req,'blockuser.html',{})

def trans(req):
 l=Trans.objects.all()
 return render(req,'trans.html',{'data':l})

def passwd(req):
 obj=Cust.objects.get(custid=101)
 return render(req,'passwd.html',{'data':obj.passwd})

def user_created(req):
 if all(list(req.POST.values())):
  obj=Cust(passwd=req.POST['passwd'],name=req.POST['name'],balance=int(req.POST['bal']),email=req.POST['email'])
  obj.save()
  send_mail(
    "New Accounts Welcome Letter",
    "Hello "+req.POST['name']+",\n\nThank you so much for allowing us to help you with your recent account opening. We are committed to providing our customers with the highest level of service and the most innovative banking products possible.\n\nWe are very glad you chose us as your financial institution and hope you will take advantage of our wide variety of savings, investment and loan products, all designed to meet your specific needs.\n\nFor more detailed information about any of our products or services, please refer to our website. or visit any of our convenient locations.\n\nValue First is a full service, locally owned financial institution. Our decisions are made right here, with this community's residents best interest in mind. We are concerned about what is best for you!\n\nPlease do not hesitate to contact me, should you have any questions. We will contact you in the very near future to ensure you are completely satisfied with the services you have received thus far\n\nFree Download\nRespectfully,\n\nPlanned pay , Always with u\n\nNew Users - please\n\nregister",
    settings.EMAIL_HOST_USER,
    [settings.EMAIL_HOST_USER,req.POST['email']],
    )
  return redirect(home)
 else:
  return render(req,'adminlog.html',{})

def search(req):
 return render(req,'search.html',{})

def locate(req):
 if not(int(req.GET['custid'])):
  return render(req,'adminlog.html',{})
 try:
  obj=Cust.objects.get(custid=req.GET['custid'])
  if obj.custid==101:
   obj=None
 except:
  obj=None
 if obj:
  if obj.status==1:
   return render(req,'edituser.html',{'form':obj})
  else:
   return render(req,'alreadyblock_user.html',{'form':obj})
 else:
  return render(req,'home.html',{'incrt':2})
   
def update_success(req):
 if not(req.POST['name']):
  return render(req,'adminlog.html',{})
 obj=Cust.objects.filter(custid=req.POST['custid'])
 obj.update(custid=int(req.POST['custid']),passwd=req.POST['passwd'],name=req.POST['name'],balance=int(req.POST['bal']),email=req.POST['email'],status=1)
 return redirect(home)

def update_passwd(req):
 if not(req.POST['passwd']):
  return render(req,'adminlog.html',{})
 obj=Cust.objects.filter(custid=101)
 obj.update(passwd=req.POST['passwd'])
 return redirect(home)

def block_success(req):
 if not(int(req.POST['custid'])):
  return render(req,'adminlog.html',{})
 custno=int(req.POST['custid'])
 try:
  obj=Cust.objects.get(custid=custno)
  if obj.status==0:
   return render(req,'home.html',{'incrt':5})
  elif obj.custid==101:
   obj=None
 except:
  obj=None
 if obj:
  obj=Cust.objects.filter(custid=custno)
  obj.update(status=0)
  return render(req,'block_success.html',{})
 else:
  return render(req,'home.html',{'incrt':2})
  
def custlog(req):
  custno=int(req.POST['custid'])
  c=Cust.objects.get(custid=custno)
  return render(req,'custlog.html',{'user':c})

def custForm(req):
  frmt='%d %B %Y'
  custno=int(req.POST['hidden_custid'])
  l=Trans.objects.all()
  c=Cust.objects.get(custid=custno)
  debit={}
  credit={}
  if 'changepasswd' in req.POST:
   return render(req,'changepasswd.html',{'user':c})
  elif 'showtrans' in req.POST:
   debit={}
   credit={}
   for i in l:
    if i.sender.custid==custno or i.receiver==custno:
     if i.sender.custid==custno:
      r=Cust.objects.get(custid=(i.receiver))
      debit[i.transid]=[{'receiverid':i.receiver},{'receivername':r.name},{'amount':i.amount},{'dot':(i.dot).strftime(frmt)}]
     else:
      s=Cust.objects.get(custid=(i.sender.custid))
      credit[i.transid]=[{'senderid':i.sender.custid},{'sendername':s.name},{'amount':i.amount},{'dot':(i.dot).strftime(frmt)}]
   return render(req,'showtrans.html',{'user':c,'cred':credit,'deb':debit})
  else:
   return render(req,'sendmoney.html',{'user':c})

def update_cust_passwd(req):
 obj=Cust.objects.filter(custid=int(req.POST['custid']))
 obj.update(passwd=req.POST['passwd'])
 return redirect(home)

def update_trans(req):
 try:
  obj=Cust.objects.get(custid=req.POST['receive'])
 except:
  return render(req, 'home.html', {'incrt':4})
 custno=int(req.POST['custid'])
 r=Cust.objects.filter(custid=int(req.POST['receive']))
 s=Cust.objects.filter(custid=custno)
 obj1=Cust.objects.get(custid=int(req.POST['receive']))
 obj2=Cust.objects.get(custid=custno)
 r.update(balance=(obj1.balance+int(req.POST['topay'])))
 s.update(balance=(obj2.balance-int(req.POST['topay'])))
 obj=Trans(sender=obj2,receiver=req.POST['receive'],amount=int(req.POST['topay']))
 obj.save()
 c=Cust.objects.get(custid=custno)
 return render(req,'custlog.html',{'user':c})

def transsearch(req):
 return render(req,'transsearch.html',{})

def locatetrans(req):
 transno=int(req.GET['transid'])
 if transno:
  try:
   obj=Trans.objects.get(transid=transno)
  except:
   return render(req,'home.html',{'incrt':1})
  return render(req,'revtrans.html',{'data':obj})
 else:
  return redirect(admin_portal)

def revtrans(req):
 transno=int(req.POST['hidden_trans'])
 if transno==0:
  return redirect(admin_portal)
 obj=Trans.objects.get(transid=transno)
 obj4=Cust.objects.get(custid=obj.sender_id)
 obj5=Cust.objects.get(custid=obj.receiver)
 obj1=Trans.objects.filter(transid=transno)
 obj2=Cust.objects.filter(custid=obj.sender_id)
 obj3=Cust.objects.filter(custid=obj.receiver)
 obj2.update(balance=(int(obj.amount)+obj4.balance))
 obj3.update(balance=(obj5.balance-int(obj.amount)))
 obj1.update(sender=obj.receiver,receiver=obj.sender_id,dot=datetime.now())
 return render(req,'home.html',{})
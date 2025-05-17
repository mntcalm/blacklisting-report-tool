import dns.resolver
import dns.reversename
import socket
import threading
import sys
from datetime import datetime
from flask import Flask, render_template, url_for


l_bl_l=open("black_lists.txt", "r")
list_blacklists=l_bl_l.readlines()
l_bl_l.close()


class Server_bulker(object): # class for server header
  def __init__(self, name, details, domains, units, time_check):
    self.name = name
    self.details = details
    self.domains = []
    self.units = []
    self.time_check = time_check

class Bulker_unit(object): # sending unit class IP+hostname from list, rest will be added every check
  def __init__(self, server, ip, hostnam, snd_score, listings, ptr_stat, a_stat, time_check):
    self.server = server
    self.ip = ip
    self.hostnam = hostnam
    self.snd_score = snd_score
    self.listings = []
    self.ptr_stat = ptr_stat #is rDNS record ok?
    self.a_stat = a_stat # is hostname ok?
    self.time_check = time_check
    
  def feel_listings(self): #метод, применяется, когда заполнено поле ip : заполняет список блеклистов, в которых ИП фигурирует
    self.listings=[]
    n_ip=self.ip
    r_ip=self.ip.split(".")[3] + "." + self.ip.split(".")[2] + "." + self.ip.split(".")[1] + "." + self.ip.split(".")[0]
    def bl_query(bl_l): # функция проверки одного ДНСобразного листинга
      try:
        dns.resolver.query(r_ip + "." + bl_l)[0]
        self.listings.append(bl_l)
      except:
        pass
    threads=[] #список для потоков, ДНС запросы буду выполняться одновременно
    for bl_l in list_blacklists:
      thread = threading.Thread(target=bl_query, args=(bl_l.rstrip("\n"),))
      threads.append(thread)
      thread.start()
    for thread in threads:
      thread.join()
class Report_unit(object): # class for report template
  def __init__(self, string, color):
    self.string = string
    self.color = color      

class Status_unit(object): # class for report template
  def __init__(self, server, string, color):
    self.server = server
    self.string = string
    self.color = color      

    
    
if len(sys.argv) > 1 and sys.argv[1] == "build":
  lst=open("list.txt", "r")
  srv_list=lst.readlines()
  lst.close()
  alarm_m=""
  stor_age=[]

  for rec in srv_list:
    if rec[0] == "-":
      srv_nam=(rec.split(" ")[0])[1:]
      srv_dtl=rec.split(" ")[1:]
      tm_ch=datetime.now().strftime("%d %B %Y %I:%M%p")
      x=Server_bulker(srv_nam, srv_dtl, [], [], tm_ch)
      stor_age.append(x)
    elif rec[0] != "" or rec[0] != " ":
      ip_u=rec.split(" ")[0]
      hstn_u=rec.split(" ")[1].rstrip("\n")
      ip_ur=ip_u.split(".")[3] + "." + ip_u.split(".")[2] + "." + ip_u.split(".")[1] + "." + ip_u.split(".")[0]
      try:
        sn_sc1=dns.resolver.query(ip_ur + "." + "score.senderscore.com")[0]
        sn_sc=str(sn_sc1).split(".")[3]
      #print(sn_sc.split(".")[3])
      except:
        sn_sc="?"
      tm_ch=datetime.now().strftime("%d %B %Y %I:%M%p")
      try:
        h_f_ip=socket.gethostbyaddr(ip_u)[0]
        h_f=" PTR is Ok, "
        if h_f_ip != hstn_u:
          h_f=" PTR is WRONG, "
          alarm_m="ALARM! "
      except:
        h_f=" PTR is DOWN, "
        alarm_m="ALARM! "
      try:
        ip_f_h=socket.gethostbyaddr(hstn_u)[2][0]
        ip_f=" hostname is Ok, "
        if ip_f_h != ip_u:
          ip_f=" hostname is WRONG, "
          alarm_m="ALARM! "
      except:
        ip_f=" hostname is DOWN, "
        alarm_m="ALARM! "
      print(ip_u, hstn_u, ip_f, h_f, sn_sc, )
      print("-----------")
      lstn=[]
      x=Bulker_unit(srv_nam, ip_u, hstn_u, sn_sc, lstn, ip_f, h_f, tm_ch)
      stor_age[(int(len(stor_age)) - 1)].units.append(x)
      stor_age[(-1)].units[(-1)].feel_listings()
    
  for serv_n in range (0, len(stor_age)):
    dmn_lst=[]
    for un_n in range (0, len(stor_age[serv_n].units)):
      print(stor_age[serv_n].units[un_n].hostnam)
      dm_nn=str(stor_age[serv_n].units[un_n].hostnam.split(".")[-2] + "." + stor_age[serv_n].units[un_n].hostnam.split(".")[-1])
      dmn_lst.append(dm_nn)
    dmn_lst=list(set(dmn_lst))  
    for i in range (0, len(dmn_lst)):
      try:
        dmm=dns.resolver.query(dmn_lst[i] + ".dbl.spamhaus.org")
        dmn_lst[i] = dmn_lst[i] + " - LISTED"
      #print(sn_sc.split(".")[3])
      except:
        pass
    stor_age[serv_n].domains=dmn_lst
  
  #--- here objects servers+units are feeled, start of report forming
  
  cmp_report=open("report.txt", "w")
  strr="Report created: " + alarm_m + str(datetime.now().strftime("%d %B %Y %I:%M%p")) + "\n"
  cmp_report.write(str(strr))
  for i in stor_age:
    strr="==> " + str(i.name) + " hidden details" + " <==\n"
    cmp_report.write(str(strr))
    for j in i.domains:
      strr=str("---\ " + j) + "\n"
      cmp_report.write(str(strr))
    for j in i.units:
      strr="----| " + str(j.ip) + " " + str(j.hostnam) + " Snd_Score: " + str(j.snd_score) + str(j.ptr_stat) + str(j.a_stat) + "LISTED " + str(len(j.listings)) + " IN: "
      #cmp_report.write(str(strr))
      for hhh in j.listings:
        strr= strr + str(str(hhh)) + " "
      strr=strr + "\n"
      cmp_report.write(str(strr))
  cmp_report.close()
else:
  app=Flask(__name__)
  
  @app.route("/")
  def index():
    
    return render_template('index.html')
  
  @app.route("/report")
  def report():
    repor=open("report.txt", "r")
    rep_un=repor.readlines()
    repor.close()
    contnt=[]
    for bl_l in rep_un:
      x=Report_unit(" ", " ")
      if bl_l[0:4] == "Repo":
        x.string=str(bl_l).rstrip("\n")
        alrm=bl_l.count("ALARM!")
        if alrm != 0:
          x.color="#ff0000"
        else:
          x.color="#001100"
        contnt.append(x)    
      elif bl_l[0:4] == "==> ": 
        x.color="#883300"
        x.string="=  Server "+str(bl_l.split(" ")[1])
        contnt.append(x)
      
      elif bl_l[0:4] == "----":
        x.string=str(bl_l[6:].rstrip("\n"))
        alrm=bl_l.count("DOWN")
        if alrm != 0:
          x.color="#ff0000"
        else:
          x.color="#007700"
        contnt.append(x)
        print(contnt[2].string)
#    for g in contnt:
#      print(g.string, g.color)
    
    return render_template('ptr_rep.html', contnt=contnt)
  
  @app.route("/status")
  def status():
    repor=open("report.txt", "r")
    rep_un=repor.readlines()
    repor.close()
    contns=[]
    for bl_l in rep_un:
      x=Report_unit(" ", " ")
      if bl_l[0:4] == "==> ":
        dd=str(bl_l.split(" ")[1])
        
      elif bl_l[0:4] == "---\\":
        x.server=dd
        x.string=str(bl_l.split(" ")[1])
        alrm=bl_l.count("LISTED")
        if alrm != 0:
          x.color="#ff0000"
        else:
          x.color="#007700"
        contns.append(x)
    return render_template('status_rep.html', contns=contns)

#  print("здесь будет сайт :\)")
#  app.run(host='0.0.0.0', port=8002, debug=True)
  app.run(host='0.0.0.0', port=8002, debug=True)
    
  

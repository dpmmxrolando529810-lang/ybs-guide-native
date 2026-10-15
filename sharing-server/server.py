"""Short-lived, explicitly approved, foreground-only location sharing.
No accounts, tracking history, analytics, access logs, or durable location storage.
Tokens are opaque capabilities; only hashes are retained in server memory.
"""
import hashlib,hmac,json,math,os,re,secrets,threading,time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer

class ApiError(Exception):
 def __init__(self,status,message): self.status,self.message=status,message

def token_hash(token):return hashlib.sha256(token.encode()).hexdigest()
class Store:
 def __init__(self,clock=time.time):self.clock=clock;self.rooms={};self.invites={};self.lock=threading.RLock();self.limits={};self.salt=secrets.token_bytes(32)
 def sweep(self):
  now=self.clock()
  for rid,r in list(self.rooms.items()):
   if r['expires_at']<=now:self.invites.pop(r['invite'],None);del self.rooms[rid]
  for key,(stamp,count) in list(self.limits.items()):
   if now-stamp>65:del self.limits[key]
 def limit(self,key,maximum):
  with self.lock:
   self.sweep();key=hashlib.sha256(self.salt+key.encode()).hexdigest();now=self.clock();stamp,n=self.limits.get(key,(now,0))
   if now-stamp>=60:stamp,n=now,0
   if n>=maximum:raise ApiError(429,'Too many requests. Please wait a minute.')
   if len(self.limits)>=20000 and key not in self.limits:raise ApiError(503,'Please try again later.')
   self.limits[key]=(stamp,n+1)
 def name(self,value):
  if not isinstance(value,str) or not 1<=len(value.strip())<=40 or any(ord(c)<32 for c in value):raise ApiError(400,'Use a name of 1 to 40 characters.')
  return value.strip()
 def create(self,p):
  with self.lock:
   self.sweep()
   if len(self.rooms)>=10000:raise ApiError(503,'Sharing is busy. Please try later.')
   duration=p.get('duration',3600)
   if type(duration) is not int or duration not in (3600,14400,28800):raise ApiError(400,'Choose one, four or eight hours.')
   name=self.name(p.get('name',''))
   rid=secrets.token_urlsafe(18);owner=secrets.token_urlsafe(32)
   invite=''.join(secrets.choice('23456789ABCDEFGHJKLMNPQRSTUVWXYZ') for _ in range(16))
   r=dict(id=rid,name=name,owner=token_hash(owner),invite=invite,invite_until=self.clock()+600,expires_at=int(self.clock()+duration),viewers={},point=None,active=False)
   self.rooms[rid]=r;self.invites[invite]=rid
   return dict(id=rid,token=owner,invite=invite,expires_at=r['expires_at'],invite_until=int(r['invite_until']),role='owner',name=name)
 def join(self,p):
  with self.lock:
   self.sweep();code=p.get('invite','')
   if not isinstance(code,str):raise ApiError(400,'Invalid invitation.')
   code=re.sub(r'[ -]','',code.upper());rid=self.invites.get(code);r=self.rooms.get(rid)
   if not r or self.clock()>r['invite_until']:raise ApiError(404,'Invitation expired or unavailable.')
   if len(r['viewers'])>=5:raise ApiError(409,'This session already has five requests. Ask the sharer to remove one.')
   name=self.name(p.get('name',''));vid=secrets.token_urlsafe(18);token=secrets.token_urlsafe(32);challenge=f'{secrets.randbelow(1000000):06d}'
   r['viewers'][vid]=dict(id=vid,name=name,token=token_hash(token),state='pending',challenge=challenge)
   return dict(id=rid,viewer_id=vid,token=token,role='viewer',name=r['name'],challenge=challenge,expires_at=r['expires_at'])
 def authorized(self,rid,token):
  self.sweep();r=self.rooms.get(rid)
  if not r:raise ApiError(410,'This sharing session has ended. Pair again to share.')
  digest=token_hash(token)
  if hmac.compare_digest(r['owner'],digest):return r,None
  for v in r['viewers'].values():
   if hmac.compare_digest(v['token'],digest):return r,v
  raise ApiError(403,'Access is not permitted.')
 def act(self,rid,token,method,action,p):
  with self.lock:
   r,v=self.authorized(rid,token);now=self.clock()
   if method=='GET' and not action:
    base=dict(id=rid,name=r['name'],expires_at=r['expires_at'],role='viewer' if v else 'owner')
    if v:
     base.update(state=v['state'],challenge=v['challenge'],viewer_id=v['id'])
     if v['state']=='approved':
      live=r['active'] and r['point'] is not None and now-r['point']['updated_at']<=90
      base.update(active=bool(live),point=r['point'] if live else None)
    else:
     base.update(invite=r['invite'] if now<=r['invite_until'] else '',invite_until=int(r['invite_until']),active=r['active'],viewers=[{k:item[k] for k in ('id','name','state','challenge')} for item in r['viewers'].values()])
    return base
   if v:
    if method=='DELETE' and action=='leave':del r['viewers'][v['id']];return {'ok':True}
    raise ApiError(403,'Only the sharer can do that.')
   if method=='DELETE' and not action:
    self.invites.pop(r['invite'],None);del self.rooms[rid];return {'ok':True}
   if method=='POST' and action in ('approve','revoke'):
    item=r['viewers'].get(p.get('viewer_id'))
    if not item:raise ApiError(404,'Viewer not found.')
    if action=='approve':item['state']='approved'
    else:del r['viewers'][item['id']]
    if not any(a['state']=='approved' for a in r['viewers'].values()):r.update(point=None,active=False)
    return {'ok':True}
   if method=='POST' and action=='pause':r.update(point=None,active=False);return {'ok':True}
   if method=='PUT' and action=='position':
    if not any(a['state']=='approved' for a in r['viewers'].values()):raise ApiError(409,'Approve a viewer before sharing location.')
    vals=[p.get(k) for k in ('lat','lng','accuracy','timestamp')]
    if any(type(x) not in (int,float) or not math.isfinite(x) for x in vals):raise ApiError(400,'Invalid location.')
    lat,lng,accuracy,stamp=vals
    if abs(lat)>90 or abs(lng)>180 or not 0<=accuracy<=5000 or now-stamp>90 or stamp-now>10:raise ApiError(400,'A recent valid GPS fix is required.')
    r.update(active=True,point=dict(lat=lat,lng=lng,accuracy=accuracy,updated_at=int(now),timestamp=int(stamp)))
    return {'ok':True}
   raise ApiError(404,'Not found.')

STORE=Store()
class Handler(BaseHTTPRequestHandler):
 server_version='YBS-Sharing/1.1';sys_version=''
 def log_message(self,*args):pass
 def do_GET(self):self.handle_api('GET')
 def do_POST(self):self.handle_api('POST')
 def do_PUT(self):self.handle_api('PUT')
 def do_DELETE(self):self.handle_api('DELETE')
 def send_json(self,status,value):
  data=json.dumps(value,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode();self.send_response(status)
  for k,v in {'Content-Type':'application/json; charset=utf-8','Content-Length':str(len(data)),'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Connection':'close'}.items():self.send_header(k,v)
  self.end_headers();self.wfile.write(data);self.close_connection=True
 def handle_api(self,method):
  self.connection.settimeout(15)
  try:
   if '?' in self.path or len(self.path)>200:raise ApiError(400,'Use the API path without query parameters.')
   if method=='GET' and self.path in ('/','/health'):return self.send_json(200,{'status':'ok','service':'YBS opt-in location sharing','version':'1.1.0','privacy':'Latest location only. Explicit viewer approval. Sessions expire within eight hours. No tracking history.'})
   body={}
   if method in ('POST','PUT'):
    try:length=int(self.headers.get('Content-Length','0'))
    except ValueError:raise ApiError(400,'Invalid content length.')
    if not 1<=length<=8192:raise ApiError(413,'Invalid request size.')
    if self.headers.get_content_type()!='application/json':raise ApiError(415,'Use JSON.')
    try:body=json.loads(self.rfile.read(length),parse_constant=lambda _:None)
    except (ValueError,UnicodeDecodeError):raise ApiError(400,'Invalid JSON.')
    if not isinstance(body,dict):raise ApiError(400,'Use a JSON object.')
   ip=self.client_address[0] # Hashed immediately by the bounded limiter; never logged or stored as an address.
   if method=='POST' and self.path=='/v1/shares':STORE.limit('create:'+ip,20);return self.send_json(201,STORE.create(body))
   if method=='POST' and self.path=='/v1/join':STORE.limit('join:'+ip,120);return self.send_json(201,STORE.join(body))
   match=re.fullmatch(r'/v1/shares/([A-Za-z0-9_-]{24})(?:/(approve|revoke|pause|position|leave))?',self.path)
   if not match:raise ApiError(404,'Not found.')
   auth=self.headers.get('Authorization','')
   if not re.fullmatch(r'Bearer [A-Za-z0-9_-]{43}',auth):raise ApiError(401,'A valid access token is required.')
   token=auth[7:];STORE.limit('token:'+token_hash(token),300)
   self.send_json(200,STORE.act(match[1],token,method,match[2] or '',body))
  except ApiError as e:self.send_json(e.status,{'error':e.message})
  except (ConnectionError,TimeoutError):self.close_connection=True
  except Exception:self.send_json(500,{'error':'Sharing temporarily unavailable.'})

class BoundedServer(ThreadingHTTPServer):
 daemon_threads=True;request_queue_size=64
 def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.slots=threading.BoundedSemaphore(64)
 def process_request(self,request,address):
  if not self.slots.acquire(False):self.shutdown_request(request);return
  try:super().process_request(request,address)
  except Exception:self.slots.release();raise
 def process_request_thread(self,request,address):
  try:super().process_request_thread(request,address)
  finally:self.slots.release()
if __name__=='__main__':BoundedServer(('0.0.0.0',int(os.getenv('PORT','10000'))),Handler).serve_forever()

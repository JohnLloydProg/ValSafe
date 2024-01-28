from objects import User
from kivy.network.urlrequest import UrlRequest
import certifi
import requests
import json

firebaseConfig = {
            'apiKey': "AIzaSyAv_aJNfqkRgIdE-Pc7BuNgacE5a20DIbo",
            'authDomain': "valsafe-e1144.firebaseapp.com",
            'projectId': "valsafe-e1144",
            'storageBucket': "valsafe-e1144.appspot.com",
            'messagingSenderId': "567585100202",
            'appId': "1:567585100202:web:0b8ed027db837753a0dbd3",
            'measurementId': "G-FTZK6K4YC7",
            'databaseURL': 'https://valsafe-e1144-default-rtdb.asia-southeast1.firebasedatabase.app/'
        }

class Firebase:
    web_api_key = 'AIzaSyAv_aJNfqkRgIdE-Pc7BuNgacE5a20DIbo'
    database_url = 'https://valsafe-e1144-default-rtdb.asia-southeast1.firebasedatabase.app'
    signup_url = f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={web_api_key}'
    refresh_url = f"https://securetoken.googleapis.com/v1/token?key={web_api_key}"
    signin_url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={web_api_key}"

    def sign_up(self, email:str, password:str):
        sign_up_payload = {"email": email, "password": password, "returnSecureToken": True}
        sign_up_request = requests.post(self.signup_url, data=sign_up_payload)
        returned_data = json.loads(sign_up_request.content.decode())
        if sign_up_request.ok == True:
            refresh_token = returned_data['refreshToken']
            localId = returned_data['localId']
            idToken = returned_data['idToken']
            return {'refreshToken': refresh_token, 'localId': localId, 'idToken': idToken}
    
    def sign_in(self, email:str, password:str):
        sign_in_payload = {"email": email, "password": password, "returnSecureToken": True}
        sign_in_request = requests.post(self.signin_url, data=sign_in_payload)
        returned_data = json.loads(sign_in_request.content.decode())
        if sign_in_request.ok == True:
            refresh_token = returned_data['refreshToken']
            localId = returned_data['localId']
            idToken = returned_data['idToken']
            return {'refreshToken': refresh_token, 'localId': localId, 'idToken': idToken}
    
    def get_infos(self, localId, idToken):
        infos = requests.get(f'{self.database_url}/users/{localId}.json?auth={idToken}')
        return json.loads(infos.content.decode())
    
    def get_emergency_mode(self, idToken):
        emergency_mode = requests.get(f'{self.database_url}/emergency_mode.json?auth={idToken}')
        return json.loads(emergency_mode.content.decode())
    
    def post_infos(self, infos, localId, idToken):
        reply = requests.put(f'{self.database_url}/users/{localId}.json?auth={idToken}', data=json.dumps(infos), )
        return reply
    
    def get_chat(self, username, idToken):
        chat = requests.get(f'{self.database_url}/group_chats/{username}.json?auth={idToken}')
        data = json.loads(chat.content.decode())
        if data:
            return [(key, data[key]['message']) for key in data.keys()]
    
    def get_user(self, localId, idToken):
        user = requests.get(f'{self.database_url}/users/{localId}.json?auth={idToken}')
        return json.loads(user.content.decode())
    
    def post_chat(self, username, chat, number, localId, idToken):
        number = '0'*(4-len(number)) + number
        reply = requests.put(f'{self.database_url}/group_chats/{username}/{number}-{localId}.json?auth={idToken}', data=json.dumps({'message': chat}))
        return reply

    def get_relief_operations(self, idToken):
        barangays = requests.get(f'{self.database_url}/relief_operations.json?auth={idToken}')
        return json.loads(barangays.content.decode())


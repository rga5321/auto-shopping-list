import gpsoauth

email = 'registrosalvaro@gmail.com'
android_id = '0123456789abcdef'
token = 'oauth2_4/0AfrIepAidIJ390_9RgEzT12zqK54O7OpKNhWXWfxSrxxBpxR9Rvj3K_587_IknXSuKhosw' # insert the oauth_token here

master_response = gpsoauth.exchange_token(email, token, android_id)
master_token = master_response['Token']  # if there's no token check the response for more details
print(master_token)

# auth_response = gpsoauth.perform_oauth(
#     email, master_token, android_id,
#     service='sj', app='com.google.android.music',
#     client_sig='...')
# token = auth_response['Auth']
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"kevin.wandel@hotmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "[theme]
base = 'light'
primaryColor='#FF4F00'
backgroundColor='#FFFFFF'
secondaryBackgroundColor='#DCDCDC'
textColor='#000000'
font='sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml


mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"kevin.wandel@hotmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "[theme]
primaryColor='#FC776A'
backgroundColor='#252525'
secondaryBackgroundColor='#444444'
textColor='#FFFFFF'
font='sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
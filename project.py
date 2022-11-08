import streamlit as st
import sqlite3
import pandas as pd
import streamlit.components.v1 as components

con = sqlite3.connect('db.db')
cur = con.cursor()

st.set_page_config(
    page_title='JYM',
    page_icon='😎',
    layout='wide',
    initial_sidebar_state='collapsed'
)

def login_user(id, pwd):
    cur.execute(f"SELECT * FROM users WHERE id='{id}' and pw='{pwd}' ")
    return cur.fetchone()


menu= st.sidebar.selectbox('MENU', options=['회원가입','로그인','회원목록', '생필품', '전자기기', '훌륭한 대화수단'])

def foodCard(menu):
    result = ''
    for value in data:
        if value['category'] == menu:
            result = result + f"""
        <div class="col">    
            <div class="card" style="width: 18rem;">
                <img src="{value['url']}" width="200px" height="200px" class="card-img-top" alt="...">
                <div class="card-body">
                <h5 class="card-title">{value['name']}</h5>
                <p class="card-text">{value['price']}</p>
                </div>
            </div>
        </div>
    """
    return result



if menu == '회원가입':
    with st.form('my_form', clear_on_submit=True):
        id = st.text_input('아이디')
        pw = st.text_input('비밀번호')
        pw_ck = st.text_input('비밀번호 확인')
        name = st.text_input('이름')
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.text_input('나이')
        with col2:
            gender = st.radio('성별',['남자','여자'], horizontal=True)
        number = st.text_input('전화번호')
        register = st.form_submit_button('회원가입')


        if register:
            cur.execute(f"INSERT INTO users(id, pw, name, age, gender, number)" f"VALUES("f" '{id}','{pw}', '{name}', {age}, '{gender}', '{number}')")
            if pw != pw_ck:
                st.warning('비밀번호가 일치하지 않습니다.')
            else:
                st.write('비밀번호가 일치합니다.')
            con.commit()
            st.success('회원가입이 완료되었습니다.')


if menu == '로그인':
   login_id= st.sidebar.text_input('아이디')
   login_pw = st.sidebar.text_input('비밀번호', type='password')
   login_btn = st.sidebar.button('로그인')
   if login_btn:
       user_info = login_user(login_id, login_pw)
       if user_info:
           st.write(user_info[2] + '님 환영합니다')
       else:
           st.write('다시 입력하세요')

if menu == '회원목록':
    st.subheader('회원목록')
    df = pd.read_sql("SELECT name, age, gender FROM users", con)
    st.dataframe(df, width=400)


data = [
    {
        'category' : '생필품',
        'url':'data:image/jpeg;base64,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',
        'name':'세제',
        'price':'12,000원'
    },
    {
        'category' : '생필품',
        'url':'http://img.danawa.com/prod_img/500000/331/563/img/14563331_1.jpg?_v=20210806153217',
        'name':'마스크',
        'price':'13,280원'

    },
    {
        'category' : '생필품',
        'url':'data:image/jpeg;base64,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',
        'name':'휴지',
        'price':'5,000원'

    },
    {
        'category' : '전자기기',
        'url':'https://blog.kakaocdn.net/dn/bRa1w6/btq5u3kUlBi/xNMgMbAfsnKJ4VShwhwHdK/img.jpg',
        'name':'아이패드 프로',
        'price':'1,249,000원부터'
    },
    {
        'category' : '전자기기',
        'url':'https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/iphone-14-pro-finish-unselect-gallery-1-202209?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=1660754213396',
        'name':'iPhone 14 Pro',
        'price':'1,550,000원부터'
    },
{
        'category' : '전자기기',
        'url':'https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/MQD83?wid=2000&hei=2000&fmt=jpeg&qlt=95&.v=1660803972361',
        'name':'에어팟 프로 2세대',
        'price':'359,000원'
    },
    {
        'category' : '훌륭한 대화수단',
        'url':'https://www.airsoftmorava.cz/files/upload/1105/pr/FB4034(1)_z1.JPG',
        'name':'AR-15',
        'price':'$1049'
    },
    {
        'category' : '훌륭한 대화수단',
        'url':'http://img.bemil.chosun.com/site/data/img_dir/2019/06/24/2019062401026_0.jpg',
        'name':'RPG-7',
        'price':'$2,500'
    },
    {
        'category' : '훌륭한 대화수단',
        'url':'data:image/jpeg;base64,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',
        'name':'Glock 17',
        'price':'$499'
    },
]


food = '짜장면'

components.html(
    f"""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>

<div class="container">
  <div class="row">
    {foodCard(menu = menu)}
  </div>
</div>
""", height=800
)


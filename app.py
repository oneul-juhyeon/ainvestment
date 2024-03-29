import streamlit as st
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import openai

def generate_seo_post(keyword, title, anchor_text, link_url):
    prompt = f"주제: {keyword}\n제목: {title}\n앵커텍스트: {anchor_text}\n링크: {link_url}\n\nSEO에 최적화된 블로그 글을 생성해 주세요. 글자 수는 1500~2000자로 제한하고, 노팔로우와 노스폰서 조건을 만족시켜 주세요."
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    post_content = response.choices[0].message['content'].strip()
    return post_content

def create_wordpress_post(wp_url, wp_username, wp_password, keyword, title, anchor_text, link_url):
    post_content = generate_seo_post(keyword, title, anchor_text, link_url)

    client = Client(wp_url, wp_username, wp_password)

    post = WordPressPost()
    post.title = title
    post.content = post_content
    post.terms_names = {
        'post_tag': ['AI', 'GPT'],
        'category': ['블로그']
    }
    post.custom_fields = []
    post.custom_fields.append({
        'key': 'external_url',
        'value': f'<a href="{link_url}" rel="nofollow nosponsored">{anchor_text}</a>'
    })

    post_id = client.call(NewPost(post))
    return post_id

def main():
    st.title("포스트인컴 자동화 웹앱")

    menu = ["글밥용", "트위터 자동 업로드", "SEO용 글 작성"]
    choice = st.sidebar.selectbox("메뉴를 선택하세요", menu)

    if choice == "글밥용":
        st.subheader("글밥용 블로그 글 생성")

        wp_url = st.text_input("워드프레스 사이트 주소")
        wp_username = st.text_input("워드프레스 사용자 이름")
        wp_password = st.text_input("워드프레스 사용자 비밀번호", type="password")
        openai.api_key = st.text_input("OpenAI API 키", type="password")

        keyword = st.text_input("키워드를 입력하세요")
        title = st.text_input("키워드 제목을 입력하세요")
        anchor_text = st.text_input("앵커 텍스트를 입력하세요")
        link_url = st.text_input("링크 주소를 입력하세요")

        if st.button("생성"):
            if wp_url and wp_username and wp_password and openai.api_key and keyword and title and anchor_text and link_url:
                post_id = create_wordpress_post(wp_url, wp_username, wp_password, keyword, title, anchor_text, link_url)
                st.success(f"블로그 글이 성공적으로 생성되었습니다! (포스트 ID: {post_id})")
            else:
                st.warning("모든 입력란을 채워주세요.")

    elif choice == "트위터 자동 업로드":
        st.subheader("트위터 게시물 자동 업로드")
        st.warning("트위터 자동 업로드 기능은 아직 구현 중입니다.")

    else:
        st.subheader("SEO 최적화 글 작성")
        st.warning("SEO 최적화 글 작성 기능은 아직 구현 중입니다.")

if __name__ == '__main__':
    main()

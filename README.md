# 앱 기본설정(임시)

최상위 디렉토리 : 제목 토글2
상위 디렉토리 (app): 제목 토글3
하위 디렉토리 :  토글
하위 파일: 글머리 기호

<aside>
💡 Ctrl + E : 인라인 코드    /     Ctrl + alt + 8 : 코드 블록

</aside>

---

`아래 토글을 열어서 확인해 주세요.`

## pjt_15/ `(프로젝트 명)`

### pjt/ `(기본 프로젝트 폴더)`

- urls.py
    
    
- views.py
- settings.py

### accounts/

- urls.py
    
    **`app_name = “accounts”`**
    
    - 회원 목록 : `path(”index/”, views.index , name=”index”)`
    - 회원 상세 정보 : `path(”<int:pk>/”, views.detail , name=”detail”)`
    - 회원 정보 수정 : `path(”edit/”, views.edit, name=”edit”)`
    - 회원 가입 : `path(”signup/”, views.signup, name=”signup”)`
    - 회원 탈퇴 : `path(”delete/”, views.delete, name=”delete”)`
    - 로그아웃 : `path(”logout/”, views.logout, name=”logout”)`
    - 비밀번호 변경 : `path(”password_change/”, views.password_change, name=”password_change”)`
- views.py
    
    회원 목록 : `index`
    
    회원 상세 정보  : `detail`
    
    회원 정보 수정 : `edit`
    
    회원 가입 : `signup`
    
    회원 탈퇴 : `delete`
    
    로그아웃 : `logout`
    
    비밀번호 변경 : `password_change`
    
- models.py
    
    모델 이름 : `User`
    
    | 이름 | 필드 | 속성 |  |
    | --- | --- | --- | --- |
    | AbstractUser사용 | - | - |  |
    | nickname | CharField |  |  |
    | profile | ImageField |  |  |
    
    ---
    
    모델 이름 : `Article`
    
    | 이름 | 필드 | 속성 |  |
    | --- | --- | --- | --- |
    | title | CharField | max_length=80 |  |
    | content | TextField |  |  |
    | image | ImageField |  |  |
    | map | ? | ? | 네이버API |
    | created_at | DateTime | auto_now_add = True |  |
    | updated_at | DateTime | auto_now = True |  |
    
    ---
    
    모델 이름 : `Comments`
    
    | 이름 | 필드 | 속성 |  |
    | --- | --- | --- | --- |
    | content | TextField |  |  |
    | react | IntegerField |  |  |
    | article | ForeiginKey |  |  |
- forms.py
    
    ```python
    class CustomUserCreationForm(UserCreationForm):
        class Meta:
            model = get_user_model()
            fields = (
                "username",
                "email",
            )
    
    class ...
    ```
    

### articles/

- urls.py
    
    **`app_name = “articles”`**
    
    ---
    
    게시글 목록 : `path(”index/”, views.index , name=”index”)`
    
    게시글 상세 정보 : `path(”<int:pk>/”, views.detail , name=”detail”)`
    
    게시글 작성 : `path(”create/”, views.create , name=”create”)`
    
    게시글 수정 : `path(”<int:pk>/edit/”, views.edit , name=”edit”)`
    
    게시글 삭제 : `path(”<int:pk>/delete”, views.delete , name=”delete”)`
    
    ---
    
    댓글 작성 : `path(”<int:pk>/comment_create/”, views.comment_create , name=”comment_create”)`
    
    댓글 수정 : `path(”<int:pk>/comment_edit”, views.comment_edit , name=”comment_edit”)`
    
    댓글 삭제 : `path(”<int:pk>/comment_delete/<int:comment_pk>”, views.comment_delete , name=”comment_delete”)`
    
- views.py
    
    ---
    
    - 게시글 목록 : `index`
    - 게시글 상세 정보 : `detail`
    - 게시글 작성 : `create`
    - 게시글 수정 : `edit`
    - 게시글 삭제 : `delete`
    
    ---
    
    - 댓글 작성 : `comment_create`
    - 댓글 수정 : `comment_edit`
    - 댓글 삭제 : `comment_delete`
    
- models.py
    
    ---
    
    모델 이름 : `Article`
    
    | 이름 | 필드 | 속성 |  |
    | --- | --- | --- | --- |
    | title | CharField |  |  |
    | content | TextField |  |  |
    | image | ImageField |  |  |
    | map | ? | ? | 네이버API |
    | created_at | DateTimeField | auto_now_add = True |  |
    | updated_at | DateTimeField | auto_now = True |  |
    
    ---
    
    모델 이름 : `Comments`
    
    | 이름 | 필드 | 속성 |  |
    | --- | --- | --- | --- |
    |  |  |  |  |
    |  |  |  |  |
    |  |  |  |  |
    |  |  |  |  |
    |  |  |  |  |
    |  |  |  |  |
- forms.py
    
    ```python
    class ArticleForm(forms.ModelForm):
        class Meta:
            model = Article
            fields = "__all__"
    				exclude = 
    
    class ...
    ```
    

---

- templates/
    - base.html
- venv/
- db.sqlite3
- manage.py
- requirements.txt
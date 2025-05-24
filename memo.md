["""
site 구성
main_page=login_page
    site_intro
    mebo(memo_board)
    lec_note(lecture_note)
    blog

main_page 구성
(=login_page)
*gate_page*
base.html 사용(site_intro 제외 login 필요)
center ==> id&pw
"""]

//how to configure memo_board
$implemented || ht_index
index page: 
    shows_only:
        admin: 전체
        other_accounts: author

$implemented || ht_d
detail_page:
    shows_only:
        admin: 전체
        other_accounts: author

$implemented || ht_md
modifydelete_page:
    shows_only:
        admin: 전체
        other_accounts: author

{start class:hts}
ht_md:
    implement_method: "if request.user != memo.author and not request.user.is_superuser:"


ht_index:
    implement_method:
<


>


ht_d:
    implement_method: 

{end class:hts}
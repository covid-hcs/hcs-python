from hcskr.hcskr import selfcheck

name = input("이름을 입력하세요: ")
birth = input("생년월일을 입력하세요: ")
level = input("학교종류를 입력하세요(예: 초등학교, 중학교, 고등학교): ")
region = input("지역을 입력하세요(예: 서울, 경기, 전남....): ")
school = input("학교이름을 입력하세요(예: 두둥실고): ")
password = input("비밀번호를 입력하세요: ")
data = selfcheck(name,birth,region,school,level,password)

print(data['message'])

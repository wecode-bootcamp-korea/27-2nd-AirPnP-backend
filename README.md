# 27-1st-airPnP-backend
> airbnb(www.https://www.airbnb.co.kr/)는 숙박공유 비즈니스입니다.
> airpnp는 숙소를 대여하는 것이 아닌 특정 재능을 가진 사람을 대여하는 것으로 프로젝트를 기획 하였습니다.

</br>

## 개발인원 및 기간
- 개발기간 : 2021-12-13 ~ 2021-12-23
- Front-end : (https://github.com/wecode-bootcamp-korea/27-2nd-AirPnP-frontend.git)
- Back-end : 김은혜, 염기욱, 이주명
  공통  : ERD/Modeling, AWS(EC2, RDS)
  김은혜 : Social SignIn, 인가 Decorator, HostSignIn, Geocoder활용 하여 주소변환, Docker 배포
  염기욱 : API Document, HostListView, HostDetailView
  이주명 : Database, BookingView, AWS의 S3 및 boto3활용한 ImageHandler

## 협업 도구
- slack
- Github
- Trello

## 적용 기술
- Python, Django, MySQL, AWS(EC2, RDS, S3), Docker, Git

## library
- JWT, Boto3, Geocoder, faker

## 구현 기능

### User
- Social SignIn : 카카오 API를 활용한 소셜 로그인 구현
- Decorator : 로그인시 JWT 토큰 발행 및 토큰 인가로 호스트 등록
- Filtering : 필터링을 통한 호스트 검색_카테고리, 위도 경도를 통한 호스트 위치, 예약 가능 날짜
- ImageHandler : S3를 활용한 이미지 업로더 구현(여러 장 업로드 가능)

### Booking
- 필터를 통한 예약 가능한 날짜로 예약 및 예약번호 출력

## ERD
<img width="1018" alt="2ndProject_wecode.png" src="./2ndProject_wecode.png">

## Reference
- API Document(https://docs.google.com/spreadsheets/d/13lN96EICsWmgxzHQCBqDGXE2Bxc1LshyV1XEfqyjpXg/edit#gid=982449144)
- 이 프로젝트는 [**airPnP**](www.https://www.airbnb.co.kr/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무 수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제가 될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
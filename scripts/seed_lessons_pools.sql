-- =========================================================
-- seed_lessons_pools.sql
-- pools 8개 / lessons 16개 / 이미지 포함
-- 실행 순서: pools → pool_images → lessons → lesson_images
-- =========================================================

-- 이미지 URL
-- pool/academy/instructor: swimpool_default.png
-- lesson_img_url / lesson_images: lesson_default.png

-- =========================================================
-- 1. pools
-- =========================================================
INSERT INTO pools (pool_name, pool_address, region, operating_hours, closing_days, contact, lane_length, lane_count, max_depth, min_depth, facilities, latitude, longitude)
VALUES
  ('잠실종합운동장 수영장', '서울 송파구 올림픽로 25',          '서울/송파', '평일 06:00~22:00 / 주말 09:00~18:00', '매주 월요일', '02-2057-0700', 50, 8,  1.80, 1.20, '샤워실, 사우나, 주차장', 37.5159, 127.0731),
  ('올림픽수영장',           '서울 송파구 방이동 88',             '서울/송파', '평일 06:00~21:00 / 주말 09:00~17:00', '매주 월요일', '02-410-1333',  50, 10, 2.00, 1.40, '샤워실, 라커, 주차장',   37.5217, 127.1220),
  ('목동실내수영장',         '서울 양천구 목동서로 225',           '서울/양천', '평일 06:00~22:00 / 주말 09:00~18:00', '매주 화요일', '02-2606-5050', 25, 6,  1.60, 1.20, '샤워실, 주차장',         37.5268, 126.8748),
  ('청담레포츠센터',         '서울 강남구 영동대로51길 14',         '서울/강남', '평일 06:00~22:00 / 주말 09:00~17:00', '매주 월요일', '02-548-2000',  25, 6,  1.60, 1.20, '샤워실, 사우나',         37.5220, 127.0536),
  ('마린스포츠센터',         '서울 강서구 공항대로 200',            '서울/강서', '평일 06:00~22:00 / 주말 09:00~18:00', '매주 목요일', '02-2606-5151', 25, 5,  1.50, 1.20, '샤워실, 주차장',         37.5598, 126.8309),
  ('강동구민체육센터 수영장', '서울 강동구 성안로 51',              '서울/강동', '평일 06:00~22:00 / 주말 09:00~18:00', '매주 월요일', '02-487-5353',  25, 6,  1.60, 1.20, '샤워실, 라커, 주차장',   37.5496, 127.1469),
  ('노원구민체육센터 수영장', '서울 노원구 동일로 1321',             '서울/노원', '평일 06:00~21:00 / 주말 09:00~17:00', '매주 수요일', '02-950-3456',  25, 6,  1.60, 1.20, '샤워실, 주차장',         37.6544, 127.0562),
  ('성북구청 수영장',        '서울 성북구 보문로 168',              '서울/성북', '평일 06:00~22:00 / 주말 09:00~18:00', '매주 화요일', '02-920-3000',  25, 5,  1.50, 1.20, '샤워실, 주차장',         37.6063, 127.0160);

-- =========================================================
-- 2. pool_images
-- =========================================================
INSERT INTO pool_images (pool_id, image_url, rep_image, sort_order)
VALUES
  (1, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', true,  0),
  (1, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', false, 1),
  (2, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', true,  0),
  (2, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', false, 1),
  (3, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', true,  0),
  (3, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', false, 1),
  (4, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', true,  0),
  (4, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', false, 1),
  (5, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', true,  0),
  (5, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', false, 1),
  (6, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', true,  0),
  (6, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', false, 1),
  (7, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', true,  0),
  (7, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', false, 1),
  (8, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', true,  0),
  (8, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png', false, 1);

-- =========================================================
-- 3. lessons
-- 컬럼 순서: pool_id, academy_id, academy_name, academy_image_url, academy_info,
--            lesson_name, level, keyword, price, capacity, lesson_schedule, lesson_status,
--            lesson_detail,
--            instructor_name, instructor_img_url, lesson_img_url, view_cnt
-- =========================================================
INSERT INTO lessons (
  pool_id, academy_id, academy_name, academy_image_url, academy_info,
  lesson_name, level, keyword, price, capacity, lesson_schedule, lesson_status,
  lesson_detail,
  instructor_name, instructor_img_url, lesson_img_url, view_cnt
)
VALUES

-- 아카데미 1: 수달상회 (pool 1 잠실)
(1, 1, '수달상회',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '서울 송파구 기반 성인 수영 전문 아카데미',
 '주말 자유수영 클래스', '초급', '#성인 #초급 #자유수영', '월 120,000원', '최대 8명', '토/일 09:00~10:30', 'OPEN',
 '{"topic":"주말 오전 자유수영 + 코칭","eligibilityRequirements":["만 18세 이상","기초 영법 가능자"],"introduction":"주말 오전 한적한 시간대 수영을 즐기실 분께 추천드려요.","applicationMethod":[{"applyUrl":"https://sudal.example.com/apply","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불","3일 전: 50% 환불"]}',
 '김수달',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 320),

(1, 1, '수달상회',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '서울 송파구 기반 성인 수영 전문 아카데미',
 '평일 마스터즈 훈련반', '고급', '#성인 #고급 #마스터즈', '월 180,000원', '최대 6명', '월/수/금 06:00~07:30', 'OPEN',
 '{"topic":"마스터즈 대회 대비 훈련","eligibilityRequirements":["4영법 가능자","주 3회 이상 참여 가능자"],"introduction":"대회 출전을 목표로 하는 성인 선수반입니다.","applicationMethod":[{"applyUrl":"https://sudal.example.com/masters","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불","3일 전: 50% 환불"]}',
 '김수달',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 210),

-- 아카데미 2: 이지스윔 (pool 2 올림픽)
(2, 2, '이지스윔',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '올림픽 레인에서 즐기는 체계적인 수영 교육',
 '성인 초보반', '초급', '#성인 #초보 #기초', '월 100,000원', '최대 10명', '화/목 19:00~20:00', 'OPEN',
 '{"topic":"수영 기초부터 차근차근","eligibilityRequirements":["수영 경험 없어도 OK"],"introduction":"수영이 처음이신 분들을 위한 기초반입니다.","applicationMethod":[{"applyUrl":"https://ezswim.example.com","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불"]}',
 '이수연',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 450),

(2, 2, '이지스윔',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '올림픽 레인에서 즐기는 체계적인 수영 교육',
 '접영 집중 클래스', '중급', '#성인 #중급 #접영', '월 150,000원', '최대 6명', '월/수 20:00~21:00', 'OPEN',
 '{"topic":"접영 마스터하기","eligibilityRequirements":["자유형/배영 가능자"],"introduction":"접영만 집중적으로 파고드는 특화반입니다.","applicationMethod":[{"applyUrl":"https://ezswim.example.com/butterfly","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 5일 전: 100% 환불"]}',
 '이수연',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 180),

-- 아카데미 3: 물곰TV스쿨 (pool 3 목동)
(3, 3, '물곰TV스쿨',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '유튜브 인기 수영 채널 물곰TV의 오프라인 클래스',
 '유튜브 연계 기초반', '초급', '#성인 #초급 #유튜브', '월 130,000원', '최대 12명', '토 10:00~11:30', 'OPEN',
 '{"topic":"영상으로 배우고 레인에서 완성","eligibilityRequirements":["만 18세 이상"],"introduction":"물곰TV 영상과 연계된 오프라인 수업입니다.","applicationMethod":[{"applyUrl":"https://mulgom.example.com","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불","3일 전: 50% 환불"]}',
 '박물곰',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 680),

(3, 3, '물곰TV스쿨',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '유튜브 인기 수영 채널 물곰TV의 오프라인 클래스',
 '영법 교정 집중반', '중급', '#성인 #중급 #교정', '월 160,000원', '최대 6명', '일 14:00~15:30', 'OPEN',
 '{"topic":"나쁜 습관 교정, 효율적인 영법 완성","eligibilityRequirements":["4영법 기본 가능자"],"introduction":"잘못된 자세를 교정하고 효율적으로 수영하는 법을 배워요.","applicationMethod":[{"applyUrl":"https://mulgom.example.com/correction","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불"]}',
 '박물곰',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 290),

-- 아카데미 4: 4레인클럽 (pool 4 청담)
(4, 4, '4레인클럽',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '강남 프리미엄 수영 클럽',
 '강남 직장인 점심 수영반', '초급', '#직장인 #점심 #강남', '월 140,000원', '최대 8명', '월~금 12:00~13:00', 'OPEN',
 '{"topic":"점심시간 활용 수영","eligibilityRequirements":["성인 누구나"],"introduction":"강남 직장인을 위한 점심 수영반. 샤워 시설 완비로 바로 복귀 가능합니다.","applicationMethod":[{"applyUrl":"https://4lane.example.com","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불"]}',
 '최레인',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 520),

(4, 4, '4레인클럽',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '강남 프리미엄 수영 클럽',
 '프리미엄 1:1 레슨', '전체', '#1대1 #프리미엄 #맞춤', '회당 80,000원', '1명', '협의 후 결정', 'OPEN',
 '{"topic":"나만을 위한 맞춤 수영 코칭","eligibilityRequirements":["레벨 무관"],"introduction":"개인 맞춤형 1:1 레슨으로 가장 빠르게 실력을 올릴 수 있습니다.","applicationMethod":[{"applyUrl":"https://4lane.example.com/private","applyUrlType":"WEB"}],"refundPolicy":["수업 24시간 전 취소 시 100% 환불"]}',
 '최레인',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 140),

-- 아카데미 5: 블루웨이브 (pool 5 마린)
(5, 5, '블루웨이브',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '서울 강서 기반 수영 전문 아카데미',
 '성인 중급 영법 완성반', '중급', '#성인 #중급 #4영법', '월 130,000원', '최대 8명', '화/목 20:00~21:30', 'OPEN',
 '{"topic":"4영법 완성 과정","eligibilityRequirements":["자유형 25m 가능자"],"introduction":"자유형부터 접영까지 4영법을 체계적으로 완성하는 과정입니다.","applicationMethod":[{"applyUrl":"https://bluewave.example.com","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불","3일 전: 50% 환불"]}',
 '정파랑',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 370),

(5, 5, '블루웨이브',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '서울 강서 기반 수영 전문 아카데미',
 '수영 다이어트반', '초급', '#성인 #다이어트 #건강', '월 110,000원', '최대 12명', '월/수/금 19:00~20:00', 'OPEN',
 '{"topic":"수영으로 건강하게 체중 관리","eligibilityRequirements":["성인 누구나"],"introduction":"유산소와 근력 강화를 동시에 할 수 있는 수영 다이어트반입니다.","applicationMethod":[{"applyUrl":"https://bluewave.example.com/diet","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불"]}',
 '정파랑',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 580),

-- 아카데미 6: 아쿠아짐 (pool 6 강동)
(6, 6, '아쿠아짐',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '강동구 대표 수중 운동 전문 센터',
 '아쿠아로빅 기초반', '초급', '#아쿠아로빅 #건강 #여성', '월 90,000원', '최대 15명', '월/수/금 10:00~11:00', 'OPEN',
 '{"topic":"물속에서 즐기는 에어로빅","eligibilityRequirements":["만 18세 이상"],"introduction":"관절에 부담 없이 즐길 수 있는 아쿠아로빅으로 건강과 활력을 되찾으세요.","applicationMethod":[{"applyUrl":"https://aquagym.example.com","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불"]}',
 '한아쿠아',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 240),

(6, 6, '아쿠아짐',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '강동구 대표 수중 운동 전문 센터',
 '시니어 수중 재활반', '초급', '#시니어 #재활 #건강', '월 100,000원', '최대 10명', '화/목 10:00~11:00', 'OPEN',
 '{"topic":"안전하고 건강한 수중 재활 운동","eligibilityRequirements":["만 50세 이상"],"introduction":"관절염, 허리 통증 등이 있는 시니어분들을 위한 전문 수중 재활반입니다.","applicationMethod":[{"applyUrl":"https://aquagym.example.com/senior","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불"]}',
 '한아쿠아',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 160),

-- 아카데미 7: 스윔히어로 (pool 7 노원)
(7, 7, '스윔히어로',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '노원구 어린이/청소년 수영 전문 아카데미',
 '청소년 선수반', '고급', '#청소년 #선수반 #대회', '월 200,000원', '최대 8명', '월~금 17:00~18:30', 'OPEN',
 '{"topic":"대회 출전을 위한 청소년 전문 훈련","eligibilityRequirements":["만 10세~19세","4영법 가능자"],"introduction":"수영 대회 출전을 목표로 하는 청소년을 위한 전문 훈련반입니다.","applicationMethod":[{"applyUrl":"https://swimhero.example.com","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불","3일 전: 50% 환불"]}',
 '오히어로',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 410),

(7, 7, '스윔히어로',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '노원구 어린이/청소년 수영 전문 아카데미',
 '어린이 생존수영반', '초급', '#어린이 #생존수영 #안전', '월 80,000원', '최대 12명', '토 10:00~11:00', 'OPEN',
 '{"topic":"어린이 생존 수영 교육","eligibilityRequirements":["만 6세~12세"],"introduction":"학교 생존수영 교육과 연계한 실용적인 수상 안전 교육입니다.","applicationMethod":[{"applyUrl":"https://swimhero.example.com/kids","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불"]}',
 '오히어로',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 290),

-- 아카데미 8: 오션핏 (pool 8 성북)
(8, 8, '오션핏',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '성북구 기반 수영 + 피트니스 복합 아카데미',
 '수영 + 피트니스 통합반', '중급', '#성인 #피트니스 #복합', '월 170,000원', '최대 8명', '월/수/금 07:00~08:00', 'OPEN',
 '{"topic":"수영과 드라이 트레이닝의 결합","eligibilityRequirements":["자유형 50m 가능자"],"introduction":"수영 후 드라이 트레이닝을 병행해 전신 운동 효과를 극대화하는 복합 프로그램입니다.","applicationMethod":[{"applyUrl":"https://oceanfit.example.com","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불","3일 전: 50% 환불"]}',
 '윤오션',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 350),

(8, 8, '오션핏',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 '성북구 기반 수영 + 피트니스 복합 아카데미',
 '새벽 자유 훈련반', '고급', '#성인 #고급 #새벽', '월 150,000원', '최대 6명', '월~금 06:00~07:00', 'OPEN',
 '{"topic":"새벽을 지배하는 자유 훈련","eligibilityRequirements":["4영법 능숙자"],"introduction":"코치 감독 하에 자신만의 훈련 계획으로 진행하는 고급 자유 훈련반입니다.","applicationMethod":[{"applyUrl":"https://oceanfit.example.com/dawn","applyUrlType":"WEB"}],"refundPolicy":["수업 시작 7일 전: 100% 환불"]}',
 '윤오션',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/swimpool_default.png',
 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png',
 195);

-- =========================================================
-- 4. lesson_images
-- =========================================================
INSERT INTO lesson_images (lesson_id, image_url, sort_order)
VALUES
  (1,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (1,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 1),
  (2,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (3,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (3,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 1),
  (4,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (5,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (5,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 1),
  (6,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (7,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (7,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 1),
  (8,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (9,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (9,  'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 1),
  (10, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (11, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (12, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (13, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (13, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 1),
  (14, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (15, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0),
  (15, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 1),
  (16, 'https://lqfigitmwcztuyiwjwrh.supabase.co/storage/v1/object/public/community-images/lesson_default.png', 0);

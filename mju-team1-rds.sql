create table situation (
   situation_id int primary key,
    situation_name varchar(30),
    situation_desc varchar(1000)
);

insert into situation values(0, '교내 지진 상황', '당신은 학생입니다. 당신의 앞에는 책상에 있고 당신은 의자에 앉아 수업을 듣고 있습니다. 교실에는 앞과 뒤에 출구가 있고 반대쪽에는 창문이 있습니다. 갑자기 지진이 발생하여 땅이 흔들리기 시작했습니다. 안전하게 초동조치를 수행하세요.');
insert into situation values(1, '건물내 화재 상황', '당신은 4층에서 엘리베이터를 기다리고 있는 회사원입니다. 갑자기 사이렌이 울리며 검은 연기가 자욱하게 들이닥치기 시작했습니다. 안전하게 건물 밖으로 나가기 위해 초동조치를 수행하세요.');
insert into situation values(2, '저지대 침수 상황', '당신은 반지하에 거주하는 20대 취준생입니다. 오늘 새벽부터 비가 오기 시작했고 창문으로 물이 새기 시작했습니다. 30분 뒤면 완전히 침수될 것 같습니다. 안전한 탈출을 위한 초동조치를 수행하세요.');

create table best_reaction (
   best_reaction_id int primary key,
    best_reaction_name varchar(50), 
    best_reaction_detail varchar(1000)
);

insert into best_reaction values(0, '책상 아래로 신체 보호', '책상 아래로 들어가 신체를 보호합니다');
insert into best_reaction values(1, '책상 다리를 잡고 균형 유지', '책상 다리를 잡고 균형을 유지합니다');
insert into best_reaction values(2, '계단 이용', '계단을 이용하여 밖으로 탈출합니다.');
insert into best_reaction values(3, '호흡기 보호', '물에 적신 옷으로 호흡기를 보호합니다.');
insert into best_reaction values(4, '비상구 이동', '비상구를 향해 탈출합니다.');
insert into best_reaction values(5, '전기 사고 방지', '콘센트를 모두 뽑아 흐르는 전류를 차단합니다.');
insert into best_reaction values(6, '가스 사고 방지', '가스 밸브를 잠가 가스 사고를 차단합니다.');

create table reaction_map (
   reaction_map_id int primary key,
   situation_id int,
    best_reaction_id int,
    constraint fk_situation_id foreign key (situation_id) references situation(situation_id),
   constraint fk_best_reaction_id foreign key (best_reaction_id) references best_reaction(best_reaction_id)
);

insert into reaction_map values(0, 0, 0);
insert into reaction_map values(1, 0, 1);
insert into reaction_map values(2, 1, 2);
insert into reaction_map values(3, 1, 3);
insert into reaction_map values(4, 2, 4);
insert into reaction_map values(5, 2, 5);
insert into reaction_map values(6, 2, 6);
# coding:utf-8

# 创建数据库
drop database ihome;
create database ihome charset=utf8;
use ihome;

# 创建用户表 (用户名和手机号独一无二)
create table ih_user_profile(
  up_user_id bigint not null auto_increment primary key comment '用户id',
  up_user_name varchar(50) unique not null comment '昵称',
  up_mobile char(11) unique not null comment '手机号码',
  up_password varchar(100) not null comment '密码',
  up_real_name varchar(10) comment '真实姓名',
  up_id_card varchar(18) comment '身份证',
  up_avatar varchar(200) comment '头像',
  up_admin tinyint not null default '0' comment '是否是管理员0不是,1是',
  up_ctime datetime not null default current_timestamp comment '创建时间',
  up_utime datetime not null default current_timestamp on update current_timestamp comment '更新时间'
)engine=InnoDB default charset=utf8 comment '用户信息表';

insert into ih_user_profile(up_user_name,up_mobile, up_password) values('15708181172','15708181172','7c222fb29b2927d828af22f592134e8932480637c0d');


# 创建地区信息表
create table ih_area_info(
  ai_area_id bigint auto_increment primary key not null comment '地区id',
  ai_area_name varchar(50) not null comment '地区名字',
  ai_ctime datetime not null default current_timestamp comment '创建时间'
)engine=InnoDB default charset=utf8 comment '地区信息表';


# 创建房屋信息表(用户的Id和地区的id是外键约束)
create table ih_house_info(
  hi_house_id bigint auto_increment primary key not null comment '房屋id',
  hi_user_id bigint not null comment '用户id',
  hi_title varchar(20) not null comment '房屋名称',
  hi_price int not null default '0' comment '房屋价格,单位：分',
  hi_area_id bigint not null comment '房屋的区域Id',
  hi_address varchar(100) not null default '' comment '房屋的地址',
  hi_room_count int not null default '1' comment '房屋的房间数',
  hi_acreage int not null default '0' comment '房屋的面积',
  hi_house_unit varchar(20) not null default '' comment '房屋的户型',
  hi_capacity int not null default '1' comment '可容纳人数',
  hi_beds varchar(50) not null default '' comment '床的配置',
  hi_deposite int not null default '0' comment '押金,单位：分',
  hi_min_days int not null default '1' comment '最短的入住时间',
  hi_max_days int not null default '0' comment '最长入住时间：0不限制',
  hi_order_count int not null default '0' comment '下单数量',
  hi_verify_status tinyint not null default '0' comment '审核状态0待审核1审核未通过2审核通过',
  hi_online_status tinyint not null default '1' comment '是否上线0下线,1上线',
  hi_index_image_url varchar(200) comment '房屋主图片',
  hi_ctime datetime not null default current_timestamp comment '创建时间',
  hi_dtime datetime not null default current_timestamp on update current_timestamp comment '更新时间',
  foreign key(hi_user_id) references ih_user_profile(up_user_id),
  foreign key (hi_area_id) references ih_area_info(ai_area_id)
)engine=InnoDB default charset=utf8 comment '房屋信息表';

# 创建房屋设施表(房屋的id是外键约束)
create table ih_house_facility(
  hf_id bigint auto_increment primary key not null comment '自增id',
  hf_house_id bigint not null comment '房屋的id',
  hf_facility_id int not null comment '房屋设施',
  hf_ctime datetime not null default current_timestamp comment '创建时间',
  foreign key(hf_house_id) references ih_house_info(hi_house_id)
)engine=InnoDB default charset=utf8 comment '房屋设施表';


# 创建设施目录表
create table ih_facility_catelog(
  fc_id int auto_increment primary key not null comment '自增id',
  fc_name varchar(20) not null comment '设施的名称',
  fc_ctime datetime default current_timestamp comment '创建时间'
)engine=InnoDB default charset=utf8 comment '设施目录表';


# 创建房屋图片表(房屋的id是外键约束)
create table ih_house_image(
  hi_house_image bigint auto_increment primary key not null comment '自增id',
  hi_house_id bigint not null comment '房屋的id',
  hi_url varchar(200) not null comment '图片url',
  hi_ctime datetime not null default current_timestamp comment '创建时间',
  foreign key(hi_house_id) references ih_house_info(hi_house_id)
)engine=InnoDB default charset=utf8 comment '房屋图片表';


# 创建订单表
create table ih_order_info(
  oi_order_id bigint auto_increment primary key not null comment '订单id',
  io_user_id bigint not null comment '用户id',
  io_house_id bigint not null comment '房屋id',
  oi_begin_date date not null comment '入住时间',
  oi_end_date date not null comment '离店时间',
  oi_days int not null comment '入住的天数',
  oi_house_price int not null comment '房屋的价格,单位：分',
  oi_amount int not null comment '订单总额,单位：分',
  oi_status tinyint not null default '0' comment '订单状态,0带接单1带支付2已支付3待评价4已完成',
  oi_comment text comment '订单评论',
  oi_ctime datetime not null default current_timestamp comment '创建时间',
  oi_dtime datetime not null default current_timestamp on update current_timestamp comment '更新时间',
  foreign key(io_user_id) references ih_user_profile(up_user_id),
  foreign key(io_house_id) references ih_house_info(hi_house_id)
)engine=InnoDB default charset=utf8 comment '订单信息表';
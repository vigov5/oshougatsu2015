-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: bk
-- ------------------------------------------------------
-- Server version	5.5.46-0ubuntu0.14.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('1c7342e9badb');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests`
--

DROP TABLE IF EXISTS `contests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `start_at` datetime DEFAULT NULL,
  `end_at` datetime DEFAULT NULL,
  `result_announced_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests`
--

LOCK TABLES `contests` WRITE;
/*!40000 ALTER TABLE `contests` DISABLE KEYS */;
INSERT INTO `contests` VALUES (4,'New Year Contest 4','Contest for HEDSPI Oshougatsu 2015','2016-01-12 16:42:04','2016-01-12 16:57:04','2016-01-12 16:57:04','2016-01-12 16:26:27','2016-01-12 16:26:27'),(5,'New Year Contest 5','Contest for HEDSPI Oshougatsu 2015','2016-01-12 17:07:12','2016-01-12 17:22:12','2016-01-12 17:22:12','2016-01-12 16:40:22','2016-01-12 17:07:12');
/*!40000 ALTER TABLE `contests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hints`
--

DROP TABLE IF EXISTS `hints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hints` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text,
  `is_open` tinyint(1) DEFAULT NULL,
  `problem_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `problem_id` (`problem_id`),
  CONSTRAINT `hints_ibfk_1` FOREIGN KEY (`problem_id`) REFERENCES `problems` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hints`
--

LOCK TABLES `hints` WRITE;
/*!40000 ALTER TABLE `hints` DISABLE KEYS */;
/*!40000 ALTER TABLE `hints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `problems`
--

DROP TABLE IF EXISTS `problems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `problems` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contest_id` int(11) DEFAULT NULL,
  `name_vi` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `content_vi` text COLLATE utf8_unicode_ci,
  `limited_time` int(11) DEFAULT NULL,
  `limited_memory` int(11) DEFAULT NULL,
  `limited_source_size` int(11) DEFAULT NULL,
  `starting_point` int(11) DEFAULT NULL,
  `wrong_answer_decreased_point` int(11) DEFAULT NULL,
  `slowly_decreased_interval` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `name_en` text COLLATE utf8_unicode_ci,
  `content_en` text COLLATE utf8_unicode_ci,
  `category` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `contest_id` (`contest_id`),
  CONSTRAINT `problems_ibfk_1` FOREIGN KEY (`contest_id`) REFERENCES `contests` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `problems`
--

LOCK TABLES `problems` WRITE;
/*!40000 ALTER TABLE `problems` DISABLE KEYS */;
INSERT INTO `problems` VALUES (9,5,'Left&Right',0,'<h5>Nhiệm vụ của bạn là đưa hết các mũi tên sang phía cũng màu với nó</h5>\r\n<h5>Cách chơi</h5>\r\nClick chuột vào các mũi tên để di chuyển chúng.<br>\r\nMột mũi tên chỉ có thể di chuyển tiến lên phía trước theo chiều mũi tên của nó.<br>\r\nNếu đằng trước mũi tên không có vật cản, nó sẽ tiến thêm 1 bước.<br>\r\nNếu đằng trước mũi tên có 1 vật cản, nó sẽ nhảy qua vật cản đó và tới vị trí tiếp theo.<br>\r\nNếu đằng trước mũi tên có hơn 1 vật cản, mũi tên sẽ không thể di chuyển nữa.<br>\r\nLoad lại trang web để chơi lại từ đầu.\r\n<br>\r\nĐiểm của bạn sẽ được cập nhật tự động thì hoàn thành game.',2000,262144,262144,100,0,86400000,'2016-01-12 15:35:41','2016-01-13 19:07:35','Left&Right','LR',2),(10,5,'Magic 7',0,'<h5>Nhiệm vụ của bạn là điều chỉnh bảng số hiện lên số 864192</h5>\r\n<h5>Cách chơi</h5>\r\nCó 3 nút nhấn. Nút \"0\" để restart game, nút \"+7\" để cộng 7 vào số trên bảng điện tử, nút \"x10\" là để nhân 10 vào số trên bảng điện tử.\r\n<br>\r\nĐiểm của bạn sẽ được cập nhật tự động thì hoàn thành game.',2000,262144,262144,100,0,86400000,'2016-01-12 15:35:41','2016-01-13 19:07:35','Magic 7','SM',2),(11,5,'Unblock me',1,'<h5>Nhiệm vụ của bạn là đưa khối màu xanh lá đến với hình tròn màu xanh lá</h5>\r\n<h5>Cách chơi</h5>\r\nDùng chuột để di chuyển các khối chữ nhật. Mỗi khối sẽ chỉ di chuyển được theo hướng chiều dài của nó.\r\n<br>\r\nĐiểm của bạn sẽ được cập nhật tự động thì hoàn thành game.',2000,262144,262144,200,0,86400000,'2016-01-12 15:35:41','2016-01-13 19:07:35','Unblock me','CNUB',2),(12,5,'Fill it',0,'<h5>Nhiệm vụ của bạn là làm đen toàn bộ tấm bảng</h5>\r\n<h5>Cách chơi</h5>\r\nClick chuột để chọn vị trí bắt đầu bất kỳ. Sau đó di chuyển theo một trong các hướng mũi tên hiện ra.\r\n<br>\r\nĐiểm của bạn sẽ được cập nhật tự động thì hoàn thành game.',2000,262144,262144,100,0,86400000,'2016-01-12 15:35:41','2016-01-13 19:07:35','Fill it','FI',2),(13,5,'Beez',1,'<h5>Nhiệm vụ của bạn là lấp đầy mật vào tổ ong</h5>\r\n<h5>Cách chơi</h5>\r\nDùng chuột để click vào các ô trong tổ ong. Mỗi lần click vào một ô, những ô xung quanh của ô đó sẽ thay đổi trạng thái, từ có mật sang không có và ngược lại. Ô bị click sẽ không đổi trạng thái.\r\n<br>\r\nĐiểm của bạn sẽ được cập nhật tự động thì hoàn thành game.',2000,262144,262144,200,0,86400000,'2016-01-12 15:35:41','2016-01-13 19:07:35','Beez','BN',2),(14,5,'Colorful',0,'<h5>Mục tiêu của bạn là điền màu vào cho các ô của bảng sau cho đúng quy luật<h5>\r\n<h5>Quy luật</h5>\r\n3 ô liền nhau, ngang hoặc dọc không được cùng màu với nhau\r\n<br>\r\nMỗi hàng phải có 3 màu đỏ và 3 màu xanh lá\r\n<br>\r\nMỗi cột cũng phải có 3 màu đỏ và 3 màu xanh lá\r\n<h5>Cách chơi</h5>\r\nDùng chuột để click vào các ô, để đổi hoặc xoá màu ở ô đó.\r\n<br>\r\nĐiểm của bạn sẽ được cập nhật tự động thì hoàn thành game.',2000,262144,262144,100,0,86400000,'2016-01-12 15:35:41','2016-01-13 19:07:35','Colorful','CLF',2),(15,5,'The Old Machine',0,'<h5>Nhiệm vụ của bạn là mở khoá một cỗ máy bảo mật cũ</h5>\r\n<h5>Cách chơi</h5>\r\nKéo thả những ổ khoá bên dưới lên những ổ khoá to phù hợp bên trên. Quan sát sự thay đổi của các ổ khoá to, tìm ra quy luật và chiến thắng. Điểm của bạn sẽ được tự động cập nhật khi hoàn thành trò chơi.\r\n<h5>Trạng thái chiến thắng</h5>\r\n- Cả 5 ổ khoá nhỏ đều được lắp.\r\n<br>\r\n- Ở trạng thái cuối cùng, số chấm trắng ở các ổ khoá to và ổ khoá nhỏ tương ứng với chúng phải đồng dư khi đem chia cho 6.\r\n<br>\r\nĐiểm của bạn sẽ được cập nhật tự động thì hoàn thành game.',2000,262144,262144,100,0,86400000,'2016-01-12 15:35:41','2016-01-13 19:07:35','The Old Machine','OM',2),(16,5,'Squares hater',1,'<h5>Nhiệm vụ của bạn là làm biến mất hết những ô vuông đang di chuyển</h5>\r\n<h5>Cách chơi</h5>\r\n<h5>Chắc chắn các bạn sẽ cần chơi thử vì hướng dẫn dưới đây khá khó hiểu ở lần đầu tiên</h5>\r\n<br>\r\nCác hình vuông có 3 màu khác nhau là đỏ, xanh lá và vàng cam. Riêng hình màu cam có 2 loại là loại to và loại nhỏ, hai màu còn lại chỉ có loại nhỏ. Bản đồ gồm 5 khu vực phân cách nhau bởi các chốt, ban đầu có sẵn 2 vùng màu là đỏ và xanh lá.\r\n<br>\r\nCó hai loại chốt là chốt mở (4 chốt), và chốt trộn (1 chốt). Khi click vào chốt mở, nếu hai bên chốt khác màu nhau, chốt sẽ không được mở. Nếu không phải như vậy, chốt sẽ mở và tạo thành một vùng to hơn. Đóng chốt chúng ta lại có các vùng nhỏ hơn. Chốt trộn là chốt sẽ hoà màu hai vùng hai bên. Màu xanh lá và màu đỏ sẽ trộn thành màu vàng cam. Màu vàng cam trộn với hai màu còn lại cũng thành màu vàng cam.\r\n<br>\r\nCác hình vuông sẽ biến mất khi vùng có nó có màu cùng với nó. Tuy nhiên sau khi biến mất nó cũng xoá luôn màu của vùng nó vừa mới nằm. Riêng hình vuông loại to thì phải cần 2 lần như vậy nó mới biến mất hoàn toàn.\r\n<br>\r\nĐiểm của bạn sẽ được cập nhật tự động thì hoàn thành game.',2000,262144,262144,200,0,86400000,'2016-01-12 15:35:41','2016-01-13 19:07:09','Squares hater','VCH',2),(17,5,'Running Horse',0,'<h5>Nhiệm vụ của bạn là dẫn con ngựa trên bàn cờ vua đi khắp bàn cờ và quay lại đúng điểm xuất phát</h5>\r\n<h5>Cách chơi</h5>\r\nClick chuột vào các ô để di chuyển con ngựa (theo cách di chuyển của con mã trên bàn cờ vua)<br>\r\nMỗi ô chỉ được đi qua đúng 1 lần.<br>\r\nClick chuột vào con ngựa để restart game.<br>\r\nĐiểm của bạn sẽ được cập nhật tự động sau khi hoàn thành game.',NULL,NULL,NULL,100,NULL,NULL,'2016-01-13 19:18:43','2016-01-13 19:20:50','Running Horse','RH',2);
/*!40000 ALTER TABLE `problems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `submissions`
--

DROP TABLE IF EXISTS `submissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `submissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `problem_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `language` int(11) DEFAULT NULL,
  `state` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `result_status` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `last_passed_test_case` int(11) DEFAULT NULL,
  `used_time` int(11) DEFAULT NULL,
  `used_memory` int(11) DEFAULT NULL,
  `received_point` int(11) DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `failed_test_case_result` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `problem_id` (`problem_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `submissions_ibfk_1` FOREIGN KEY (`problem_id`) REFERENCES `problems` (`id`),
  CONSTRAINT `submissions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submissions`
--

LOCK TABLES `submissions` WRITE;
/*!40000 ALTER TABLE `submissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `submissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_forgot_passwords`
--

DROP TABLE IF EXISTS `user_forgot_passwords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_forgot_passwords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `token` varchar(40) DEFAULT NULL,
  `expire_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_forgot_passwords_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_forgot_passwords`
--

LOCK TABLES `user_forgot_passwords` WRITE;
/*!40000 ALTER TABLE `user_forgot_passwords` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_forgot_passwords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_join`
--

DROP TABLE IF EXISTS `user_join`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_join` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `contest_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `contest_id` (`contest_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_join_ibfk_1` FOREIGN KEY (`contest_id`) REFERENCES `contests` (`id`),
  CONSTRAINT `user_join_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_join`
--

LOCK TABLES `user_join` WRITE;
/*!40000 ALTER TABLE `user_join` DISABLE KEYS */;
INSERT INTO `user_join` VALUES (1,19,5,'2016-01-13 18:58:38'),(2,41,5,'2016-01-13 18:58:38');
/*!40000 ALTER TABLE `user_join` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_scores`
--

DROP TABLE IF EXISTS `user_scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_scores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `contest_id` int(11) DEFAULT NULL,
  `point` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `contest_id` (`contest_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_scores_ibfk_1` FOREIGN KEY (`contest_id`) REFERENCES `contests` (`id`),
  CONSTRAINT `user_scores_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_scores`
--

LOCK TABLES `user_scores` WRITE;
/*!40000 ALTER TABLE `user_scores` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_scores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `encrypted_password` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `reset_password_token` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `reset_password_sent_at` datetime DEFAULT NULL,
  `remember_created_at` datetime DEFAULT NULL,
  `sign_in_count` int(11) NOT NULL DEFAULT '0',
  `current_sign_in_at` datetime DEFAULT NULL,
  `last_sign_in_at` datetime DEFAULT NULL,
  `current_sign_in_ip` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `last_sign_in_ip` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `locale` int(11) DEFAULT '0',
  `student_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_users_on_email` (`email`),
  UNIQUE KEY `index_users_on_reset_password_token` (`reset_password_token`)
) ENGINE=InnoDB AUTO_INCREMENT=167 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (19,'nguyen.anh.tien@framgia.com','$2a$12$kjxb9lhUT4YE0SxNlabIJOYNK6pOC.gSONGpcJ6UMCc7MthUJbxp2','86f0d0264eaf39753cf8b666a0696bd1a70ee756','2015-07-30 11:10:40',NULL,97,'2016-01-13 15:30:56','2015-12-07 18:04:54','127.0.0.1','127.0.0.1','2013-11-09 01:29:59','2016-01-13 15:30:29',0,''),(41,'tran.ba.trong@framgia.com','$2a$10$o2WqrRmFvLI2u1E1LKc9qubyv/JgKIDzg.gMbzguM4wsvLzj82k/m',NULL,NULL,NULL,42,'2016-01-13 17:46:20','2016-01-13 17:46:16','192.168.1.8','192.168.1.8','2013-11-11 10:26:33','2016-01-13 17:44:27',0,'');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-01-13 19:45:14

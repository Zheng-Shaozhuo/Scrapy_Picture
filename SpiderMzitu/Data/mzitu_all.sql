/*
Navicat MySQL Data Transfer

Source Server         : Local
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : vv_spider

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2018-07-18 12:22:00
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `mzitu_all_nn`
-- ----------------------------
DROP TABLE IF EXISTS `mzitu_all_nn`;
CREATE TABLE `mzitu_all_nn` (
  `source` varchar(32) NOT NULL,
  `type` varchar(128) NOT NULL,
  `title` varchar(128) NOT NULL,
  `page_url` varchar(128) DEFAULT NULL,
  `img_path` varchar(128) DEFAULT '',
  `state` tinyint(4) DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of mzitu_all_nn
-- ----------------------------

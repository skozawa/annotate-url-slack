SET GLOBAL innodb_file_format = Barracuda;
SET GLOBAL innodb_file_per_table = 1;
SET GLOBAL innodb_large_prefix = 1;


DROP TABLE IF EXISTS `entry`;
CREATE TABLE `entry` (
  `id` BIGINT UNSIGNED NOT NULL,
  `uri` VARCHAR(255) NOT NULL,
  `created` TIMESTAMP NOT NULL,

  PRIMARY KEY (`id`),
  UNIQUE KEY (`uri`),
  KEY (`created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `score`;
CREATE TABLE `score` (
  `entry_id` BIGINT UNSIGNED NOT NULL,
  `annotator` VARCHAR(100) NOT NULL,
  `score` MEDIUMBLOB NOT NULL,
  `created` TIMESTAMP NULL,
  `modified` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`entry_id`, `annotator`),
  KEY (`created`),
  KEY (`modified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `content`;
CREATE TABLE `content` (
  `entry_id` BIGINT UNSIGNED NOT NULL,
  `title` BLOB NOT NULL,
  `html` MEDIUMBLOB NOT NULL,
  `created` TIMESTAMP NOT NULL,

  PRIMARY KEY (`entry_id`),
  KEY (`created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

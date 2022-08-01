CREATE TABLE IF NOT EXISTS `ytvideostats` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `channelId` VARCHAR(255) NOT NULL,
    `videoId` VARCHAR(255) NOT NULL,
    `viewCount` BIGINT NOT NULL DEFAULT '0',
    `likeCount` BIGINT NOT NULL DEFAULT '0',
    `dislikeCount` BIGINT NOT NULL DEFAULT '0',
    `favoriteCount` BIGINT NOT NULL DEFAULT '0',
    `commentCount` BIGINT NOT NULL DEFAULT '0',
    `videoPerformance` DECIMAL NOT NULL DEFAULT '0',
    `updatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB;

CREATE TABLE IFNOT EXISTS `ytvideotags` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `channelId` VARCHAR(255) NOT NULL,
    `videoId` VARCHAR(255) NOT NULL,
    `tag` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB;
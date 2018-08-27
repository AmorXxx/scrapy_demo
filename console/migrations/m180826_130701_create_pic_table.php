<?php

use yii\db\Migration;

/**
 * Handles the creation of table `pic`.
 */
class m180826_130701_create_pic_table extends Migration
{
    /**
     * {@inheritdoc}
     */
    public function safeUp()
    {
        if ($this->db->driverName === 'mysql') {
            // http://stackoverflow.com/questions/766809/whats-the-difference-between-utf8-general-ci-and-utf8-unicode-ci
            $tableOptions = 'CHARACTER SET utf8 COLLATE utf8_unicode_ci ENGINE=InnoDB';
        }

        $this->createTable('{{%hupu}}', [
            'id' => $this->primaryKey(),
            'img_path' => $this->char(200)->notNull(),
        ], $tableOptions);
    }

    public function down()
    {
        $this->dropTable('{{%detail}}');
    }
}

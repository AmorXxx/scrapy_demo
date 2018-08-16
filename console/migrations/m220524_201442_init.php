<?php

use yii\db\Migration;

class m220524_201442_init extends Migration
{
    public function up()
    {
        $tableOptions = null;
        if ($this->db->driverName === 'mysql') {
            // http://stackoverflow.com/questions/766809/whats-the-difference-between-utf8-general-ci-and-utf8-unicode-ci
            $tableOptions = 'CHARACTER SET utf8 COLLATE utf8_unicode_ci ENGINE=InnoDB';
        }

        $this->createTable('{{%detail}}', [
            'id' => $this->primaryKey(),
            'package_id' => $this->bigInteger()->notNull(),
            'time' => $this->dateTime(0)->notNull(),
            'context' => $this->char(100)->notNull(),
        ], $tableOptions);
    }

    public function down()
    {
        $this->dropTable('{{%detail}}');
    }
}

<?php

namespace backend\models;

use Yii;

/**
 * This is the model class for table "{{%detail}}".
 *
 * @property int $id
 * @property string $package_id
 * @property string $time
 * @property string $contexnt
 */
class Detail extends \yii\db\ActiveRecord
{
    /**
     * @inheritdoc
     */
    public static function tableName()
    {
        return '{{%detail}}';
    }

    /**
     * @inheritdoc
     */
    public function rules()
    {
        return [
            [['package_id', 'time', 'contexnt'], 'required'],
            [['package_id'], 'integer'],
            [['time'], 'safe'],
            [['contexnt'], 'string', 'max' => 100],
        ];
    }

    /**
     * @inheritdoc
     */
    public function attributeLabels()
    {
        return [
            'id' => 'ID',
            'package_id' => 'Package ID',
            'time' => 'Time',
            'contexnt' => 'Contexnt',
        ];
    }
}

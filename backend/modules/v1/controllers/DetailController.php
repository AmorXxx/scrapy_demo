<?php
/**
 * Created by PhpStorm.
 * User: Amor
 * Date: 2018/8/8
 * Time: 9:59
 */

namespace backend\modules\v1\controllers;


use yii\rest\ActiveController;

class DetailController extends ActiveController
{
    public $modelClass = 'backend\modules\v1\models\Detail';
    public function actions()
    {
        $actions = parent::actions();

        // 禁用动作
        unset($actions['index']);
        unset($actions['delete']);
        unset($actions['create']);
        unset($actions['view']);
        unset($actions['update']);
        return $actions;
    }


    public function actionIndex(){
        header("Content-Type: text/html; charset=utf-8");
        require_once('php_python.php');
        $request=\Yii::$app->request;
        $parms=$request->get();
        $res = ppython("test::selenium_package_inquiry",$parms['package_id']);
        return $res;

    }

}
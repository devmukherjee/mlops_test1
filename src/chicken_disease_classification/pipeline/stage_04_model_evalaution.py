from src.chicken_disease_classification.config.configuration import ConfigurationManager
from src.chicken_disease_classification.constants import PARAMS_FILE_PATH,CONFIG_FILE_PATH
from src.chicken_disease_classification.components.evaluation import Evaluation
from src.chicken_disease_classification import logger



class ModelEvaluationPipeline():
    def __init__(self):
        pass
    def main(self):
        try:
            configuration_manager= ConfigurationManager(CONFIG_FILE_PATH,PARAMS_FILE_PATH)
            model_eval_config= configuration_manager.get_model_evaluation_config()
            model_evaluator= Evaluation(evaluation_config= model_eval_config)
            model_evaluator.load_model(model_evaluator.config.path_of_model)
            model_evaluator.preprocess_data()
            model_evaluator.build_additional_parameters()
            metrics_dict= Evaluation.evaluation(model= model_evaluator.model
                                    ,criterion= model_evaluator.criterion
                                    ,dataloader=model_evaluator.test_image_dataloader
                                    ,dataset_size=model_evaluator.dataset_size)
            print(metrics_dict)
            print(type(metrics_dict))
            Evaluation.save_metrics(metrics_dict=metrics_dict,path=model_eval_config.metrics_file_path)
        except Exception as e:
            logger.error(e)
            raise e

if __name__=='__main__':
    STAGE_NAME= "Evaluation Pipeline"
    try:
        logger.info(f">>>>>>>>>>>>>>>>>>>>>STAGE {STAGE_NAME} Started <<<<<<<<<<<<<<<<<<<<<<<<")
        eval_pipeline=ModelEvaluationPipeline()
        eval_pipeline.main()
        logger.info(f">>>>>>>>>>>>>>>>>>>>>STAGE {STAGE_NAME} Completed <<<<<<<<<<<<<<<<<<<<<<<<")
    except Exception as e:
        logger.error(f'STAGE: {STAGE_NAME} failed with the following exception:{e}')
        raise e

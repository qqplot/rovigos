import sys
from logging import getLogger
from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.model.general_recommender import Pop, ConvNCF, SimpleX
from recbole.model.sequential_recommender import BERT4Rec, GRU4Rec, SASRec, LightSANs, SRGNN, S3Rec
from recbole.trainer import Trainer
from recbole.utils import init_seed, init_logger
import os

MAPPER = {
    "Pop": Pop,
    "ConvNCF": ConvNCF,
    "SimpleX": SimpleX,
    "BERT4Rec": BERT4Rec, # bert
    "GRU4Rec": GRU4Rec, 
    "SASRec": SASRec, # attention/ transformer
    "LightSANs": LightSANs, # transfomer efficent
    "SRGNN": SRGNN, # GNN
    "S3Rec": S3Rec, # context 
}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main(argv):
    try:
        model_name = argv[1]
        Model = MAPPER[model_name]  
    except:
        print("[ERROR] Give model name as an argument")
        return
    
    # configurations initialization
    # global_config_file = os.path.join(BASE_DIR, 'config/config.yaml')
    global_config_file = os.path.join(BASE_DIR, 'config/config_general.yaml')
    specific_config_file = os.path.join(BASE_DIR, f'config/{model_name.lower()}.yaml')
    config_file_list = [cf for cf in [global_config_file, specific_config_file] if os.path.exists(cf)]
    config = Config(
        model=model_name,
        config_file_list=config_file_list
    )

    # init random seed
    init_seed(config['seed'], config['reproducibility'])

    # logger initialization
    init_logger(config)
    logger = getLogger()

    # write config info into log
    logger.info(config)

    # dataset creating and filtering
    dataset = create_dataset(config)
    logger.info(dataset)

    # dataset splitting
    train_data, valid_data, test_data = data_preparation(config, dataset)

    # model loading and initialization
    model = Model(config, train_data.dataset).to(config['device'])
    logger.info(model)

    # trainer loading and initialization
    trainer = Trainer(config, model)

    # model training
    best_valid_score, best_valid_result = trainer.fit(train_data, valid_data)

    # model evaluation
    test_result = trainer.evaluate(test_data)
    logger.info(test_result)


if __name__ == '__main__':
    main(sys.argv)


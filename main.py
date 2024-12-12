from Core.GraphRAG import GraphRAG
from Option.Config2 import Config
import argparse
import os
import asyncio
from pathlib import Path
from shutil import copyfile
from Data.QueryDataset import RAGQueryDataset

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

parser = argparse.ArgumentParser()
parser.add_argument("-opt", type=str, help="Path to option YMAL file.")
args = parser.parse_args()

opt = Config.parse(Path(args.opt))
digimon = GraphRAG(config=opt)


def check_dirs(opt):
    result_dir = os.path.join(
        opt.working_dir, opt.exp_name, "Results"
    )  # For each query, save the results in a separate directory
    config_dir = os.path.join(
        opt.working_dir, opt.exp_name, "Configs"
    )  # Save the current used config in a separate directory
    metric_dir = os.path.join(
        opt.working_dir, opt.exp_name, "Metrics"
    )  # Save the metrics of entire experiment in a separate directory
    os.makedirs(result_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(metric_dir, exist_ok=True)
    opt_name = args.opt[args.opt.rindex("/") + 1 :]
    basic_name = os.path.join(os.path.dirname(args.opt), "Config2.yaml")
    copyfile(args.opt, os.path.join(config_dir, opt_name))
    copyfile(basic_name, os.path.join(config_dir, "Config2.yaml"))


# corpus = read_corpus()
# dataloader = crate_dataloader(opt.dataset_name)

if __name__ == "__main__":
    check_dirs(opt)
    query_dataset = RAGQueryDataset()
    corpus = query_dataset.get_corpus()
    print(f"length of corpus: {len(corpus)}")
    corpus = corpus[:10]
    asyncio.run(digimon.insert(corpus))
    # asyncio.run(digimon.insert([doc]))

    # for train_item in dataloader:

    asyncio.run(digimon.query("Who is Scrooge?"))

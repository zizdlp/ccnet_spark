from ccnet_spark.pipe_line import Pipeline, Config,PipelineStep
import time
from pyspark.sql import SparkSession
import sys

def getPIP(index):
    pips = [
    [],
    [
        PipelineStep.REAL_LEN,
    ],
    [
        PipelineStep.REAL_LEN,
        PipelineStep.HASH
    ],
    [
        PipelineStep.REAL_LEN,
        PipelineStep.HASH,
        PipelineStep.DEDUP_KEEP
    ],
    [
        PipelineStep.REAL_LEN,
        PipelineStep.HASH,
        PipelineStep.DEDUP_KEEP,
        PipelineStep.LID,
    ],
    [
        PipelineStep.REAL_LEN,
        PipelineStep.HASH,
        PipelineStep.DEDUP_KEEP,
        PipelineStep.LID,
        PipelineStep.SP,
    ],
    [
        PipelineStep.REAL_LEN,
        PipelineStep.HASH,
        PipelineStep.DEDUP_KEEP,
        PipelineStep.LID,
        PipelineStep.SP,
        PipelineStep.LM,
    ],
    [
        PipelineStep.REAL_LEN,
        PipelineStep.HASH,
        PipelineStep.DEDUP_KEEP,
        PipelineStep.LID,
        PipelineStep.SP,
        PipelineStep.LM,
        PipelineStep.PP_BUCKET,
    ],
    [
        PipelineStep.REAL_LEN,
        PipelineStep.HASH,
        PipelineStep.DEDUP_KEEP,
        PipelineStep.LID,
        PipelineStep.SP,
        PipelineStep.LM,
        PipelineStep.PP_BUCKET,
        PipelineStep.DROP,
    ],
]
    return pips[index]

spark = (
    SparkSession.builder.appName("CCNETSpark_ONLY")
    # .master("local[*]")
    .config("spark.executor.memory", "100g")
    .config("spark.driver.memory", "100g")
    .config("spark.driver.maxResultSize", "100g")
    .config("spark.sql.execution.arrow.pyspark.enabled", "true")
    # .config("spark.executor.extraJavaOptions", "-XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps")
    # .config("spark.driver.extraJavaOptions", "-XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps")
    .getOrCreate()
)

if __name__ == "__main__":
    # 从命令行参数中获取索引
    index = int(sys.argv[1])
    pip=getPIP(index)
    print(f"pipline is:{pip}")
    config = Config(
            isSample=False,
            n_segments=1,
            sampleRate=0.01,
            cache_dir="../../cached_data/",
            output_dir="../../cached_data/",
            fasttext_model_path="../../cc_net/bin/lid.bin",
            lm_dir="../../cc_net/data/lm_sp",
            cutoff_csv_path="../../cc_net/cc_net/data/cutoff.csv",
            dump="2019-18",
            pipeline=pip,
        )
    
    pipeline = Pipeline(config,spark)
    df = pipeline.load_data()
    s = time.time()
    pipeline.run_pipeline()
    res=pipeline.df.rdd.count()
    # pipeline.save_data()
    e = time.time()
    print("==============================================")
    print(f"pipeline:{pip}, time consume:{e-s}s")

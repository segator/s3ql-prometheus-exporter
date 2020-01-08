import os
import struct
import sys
import time
import argparse
from prometheus_client import start_http_server, Metric, REGISTRY
CTRL_NAME = '.__s3ql__ctrl__'
def main(args=None):
    appParser = argparse.ArgumentParser(description='List the content of a folder',prog='s3qlprometheus',usage='%(prog)s [s3ql mount path] [options]')
    appParser.add_argument('-p','--path',metavar='s3qlMountPath',type=str,required=True,help='the path to mounted s3ql')
    appParser.add_argument('-P','--port',metavar='prometheusListenPort',type=int,default=6530,help='Prometheus listen port. DEFAULT: 6530')

    args = appParser.parse_args(args)
    ctrlfile = os.path.join(args.path, CTRL_NAME)
    start_http_server(args.port)
    REGISTRY.register(S3QLStatsCollector(ctrlfile))
    while True: time.sleep(500)

class S3QLStatsCollector(object):
    def __init__(self, ctrlfile):
        self.ctrlfile=ctrlfile

    def collect(self):
        buf = os.getxattr(self.ctrlfile, 's3qlstat')
        (entries, blocks, inodes, fs_size, dedup_size,
        compr_size, db_size, cache_cnt, cache_size, dirty_cnt,
        dirty_size, removal_cnt) = struct.unpack('QQQQQQQQQQQQ', buf)
        p_dedup = dedup_size * 100 / fs_size if fs_size else 0
        p_compr_1 = compr_size * 100 / fs_size if fs_size else 0
        p_compr_2 = compr_size * 100 / dedup_size if dedup_size else 0

        metric = Metric('s3ql_directory_entires','Directory entries', 'summary')
        metric.add_sample('s3ql_directory_entries_count',value=entries, labels={})
        yield metric

        metric = Metric('s3ql_inodes','Inodes', 'summary')
        metric.add_sample('s3ql_inodes_count',value=inodes, labels={})
        yield metric

        metric = Metric('s3ql_data_blocks','Data blocks', 'summary')
        metric.add_sample('s3ql_data_blocks_count',value=blocks, labels={})
        yield metric

        metric = Metric('s3ql_data_size','Data size', 'summary')
        metric.add_sample('s3ql_data_size_total',value=fs_size, labels={})
        metric.add_sample('s3ql_data_size_after_dedup',value=dedup_size, labels={})
        metric.add_sample('s3ql_data_size_after_dedup_percent',value=p_dedup, labels={})
        metric.add_sample('s3ql_data_size_after_compress',value=compr_size, labels={})
        metric.add_sample('s3ql_data_size_after_compress_percent_total',value=p_compr_1, labels={})
        metric.add_sample('s3ql_data_size_after_compress_percent_dedup',value=p_compr_2, labels={})
        yield metric


        metric = Metric('s3ql_database_size','Database size', 'summary')
        metric.add_sample('s3ql_database_size_count_uncompress',value=db_size, labels={})
        yield metric

        metric = Metric('s3ql_cache_size','Cache size', 'summary')
        metric.add_sample('s3ql_cache_size_count',value=cache_size, labels={})
        metric.add_sample('s3ql_cache_size_count_entries',value=cache_cnt, labels={})
        metric.add_sample('s3ql_cache_size_dirty_count',value=dirty_size, labels={})
        metric.add_sample('s3ql_cache_size_dirty_count_entries',value=dirty_cnt, labels={})
        yield metric

        metric = Metric('s3ql_queue_removal','Cache size', 'summary')
        metric.add_sample('s3ql_queue_removal_count',value=removal_cnt, labels={})
        yield metric

if __name__ == '__main__':
    main(sys.argv[1:])

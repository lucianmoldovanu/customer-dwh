from dagster import job
from PIPELINE.ops.refresh_ip_to_countries import refresh_in_batches

@job
def refresh_ip_to_countries():
    refresh_in_batches()

# testing
if __name__ == "__main__":
    refresh_ip_to_countries()
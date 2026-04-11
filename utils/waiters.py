import time


def wait_operation(
    operations_api,
    operation_id,
    timeout=15,
    interval=1
):

    start_time = time.time()

    while time.time() - start_time < timeout:
        resp = operations_api.get_status(operation_id)

        if resp.status_code != 200:
            time.sleep(interval)
            continue

        data = resp.json()
        status = data.get("status")
        if status == "success":
            return data

        if status == "failed":
            raise AssertionError(f"Operation failed: {data}")

        time.sleep(interval)

    raise TimeoutError(f"Operation {operation_id} not completed in {timeout} sec")
from test.celery_test.redis_method.redis_method import (
    redis_lock,
    post_view_count_cache_scan,
    post_view_count_cache_unlink,
    post_view_count_cache_get,
)
from test.celery_test.rabbitmq_method.rabbitmq_method import send_to_fastapi


def update_post_view_counts():
    with redis_lock("update_post_view_counts", timeout=3600) as lock:
        if lock:
            post_view_counts = dict()

            for key in post_view_count_cache_scan():
                prefix, user_id, post_id, uuid, timestamp = key.decode("utf-8").split(
                    ":"
                )
                value = post_view_count_cache_get(
                    user_id=user_id, post_id=post_id, uuid=uuid, timestamp=timestamp
                )

                post_view_counts[post_id] = post_view_counts.get(post_id, 0) + value
                post_view_count_cache_unlink(user_id, post_id, uuid, timestamp)

            for post_id, count in post_view_counts.items():
                # for update로 배타락이 걸린 경우에서의 처리 방법이 필요하다.
                # 접근이 차단된 경우, fastapi에서 value를 value로 가지는 key-value pair를 발행한다.
                # 갱신이 완료될 때 까지 해당 과정을 반복한다.

                # fastapi에 결과 전송
                send_to_fastapi(
                    message={
                        "task_key": "update_post_view_counts",
                        "post_id": post_id,
                        "count": count,
                    },
                    json_message=True,
                )

            return "Success"
        else:
            return "Ignored"

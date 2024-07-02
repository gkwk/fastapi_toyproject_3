from sqlalchemy.orm import Session

from models import Post
from database.database import get_data_base_decorator
from database.cache import (
    redis_lock,
    post_view_count_cache_scan,
    post_view_count_cache_unlink,
)


@get_data_base_decorator
def update_post_view_counts(data_base: Session):
    with redis_lock("update_post_view_counts", timeout=3600) as lock:
        if lock:
            post_view_counts = dict()

            for key in post_view_count_cache_scan():
                prefix, user_id, post_id, uuid, timestamp = key.decode("utf-8").split(
                    ":"
                )
                post_view_counts[post_id] = post_view_counts.get(post_id, 0) + 1
                post_view_count_cache_unlink(user_id, post_id, uuid, timestamp)

            for post_id, count in post_view_counts.items():
                # for update로 배타락이 걸린 경우에서의 처리 방법이 필요하다.
                # 접근이 차단된 경우, 해당 post_id는 새로운 key와 value로 redis에 추가하고, 같은 종류의 key와 value를 다루는 함수를 호출하는 식으로 처리한다.
                # 또 다시 접근이 차단된다면 value만 갱신하면서 처리가 완료될 때 까지 해당 과정을 반복한다.
                data_base.query(Post).filter(Post.id == post_id).update(
                    {Post.number_of_view: Post.number_of_view + count},
                    synchronize_session=False,
                )

            data_base.commit()

            return "Success"
        else:
            return "Ignored"

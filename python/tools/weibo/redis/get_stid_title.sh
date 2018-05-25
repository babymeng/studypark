#!/bin/bash

for stid in $(cat stid_keys)
do
    curl "http://i.api.weibo.com/2/stories/get_story_info_batch.json?source=4050779375&story_ids=$stid"
done


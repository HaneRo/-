#!/bin/bash
url="http://10.10.10.10:9090/"
password="password"
# 获取网页内容并保存到变量response中
response=$(curl $url'providers/proxies' \
  -H 'Authorization: Bearer '$password \
  --insecure
)
# 从response中提取JSON数据中的providers.default的值并保存到变量data中
data=$(echo "$response" | jq '[.providers."🖼️ Booru".proxies[] | select(.alive == true) | .name][1:]')
echo "$data"
N=$(echo "$data" | jq '. | length')

while true; do
    output=$(curl -s https://konachan.com/)
    if [[ $output == *"cf-wrapper"* || -z $output ]]; then
        echo "Found 'cf-wrapper' in the output. Repeating the loop..."
        random_number=$((RANDOM % N))
        name=$(echo "$data" | jq .[$random_number])
        curl $url'proxies/%F0%9F%96%BC%EF%B8%8F%20Booru' \
        -X 'PUT' \
        -H 'Authorization: Bearer '$password \
        --data-raw '{"name":'"$name"'}' \
        --insecure ;
        sleep 3
    else
        break
    fi
done

echo "Finished."

#!/bin/bash
url="http://10.10.10.10:9090/"
password="password"
# 获取网页内容并保存到变量response中
response=$(curl $url'proxies' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7' \
  -H 'Authorization: Bearer '$password \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: agh_session=2009f03dae627b68a3a3fbd592e47712' \
  -H 'DNT: 1' \
  -H 'Referer: http://10.10.10.10:9999/ui/yacd/' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  --compressed \
  --insecure
)
# 从response中提取JSON数据中的providers.default的值并保存到变量data中
data=$(echo "$response" | jq '.proxies."🖼️ Booru".all')
echo "$data"
echo "$data" | jq '. | length'
N=$(echo "$data" | jq '. | length')

while true; do
    output=$(curl -s https://konachan.com/)
    if [[ $output == *"cf-wrapper"* || -z $output ]]; then
        echo "Found 'cf-wrapper' in the output. Repeating the loop..."
        random_number=$((RANDOM % N))
        echo $random_number
        echo "$data" | jq .[$random_number]
        name=$(echo "$data" | jq .[$random_number])
        echo $name
        curl $url'proxies/%F0%9F%96%BC%EF%B8%8F%20Booru' \
        -X 'PUT' \
        -H 'Accept: */*' \
        -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7' \
        -H 'Authorization: Bearer '$password \
        -H 'Connection: keep-alive' \
        -H 'Content-Type: application/json' \
        -H 'Cookie: agh_session=2009f03dae627b68a3a3fbd592e47712' \
        -H 'DNT: 1' \
        -H 'Origin: http://10.10.10.10:9999' \
        -H 'Referer: http://10.10.10.10:9999/ui/yacd/' \
        -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
        --data-raw '{"name":'$name'}' \
        --compressed \
        --insecure ;
        sleep 3
    else
        break
    fi
done

echo "Finished."


output_dir := '_site'
base_url := 'https://tlgs.github.io/gcp-icons/'

build: download unzip collect render cleanup

download:
  curl -sS \
    -O https://services.google.com/fh/files/misc/core-products-icons.zip \
    -O https://services.google.com/fh/files/misc/category-icons.zip

unzip:
  unzip -q -d core-products-icons core-products-icons.zip 
  unzip -q -d category-icons category-icons.zip 

collect:
  mkdir -p {{output_dir}}/core {{output_dir}}/category
  find core-products-icons -type f -regextype posix-extended -iregex ".*\.(png|svg)$" -exec mv -t {{output_dir}}/core {} +
  find category-icons -type f -regextype posix-extended -iregex ".*\.(png|svg)$" -exec mv -t {{output_dir}}/category {} +

render url_prefix=base_url:
  uv run main.py --url-prefix {{url_prefix}} --top-dir {{output_dir}} 

cleanup:
  rm -rf core-products-icons category-icons *.zip

serve: (render "http://localhost:8000/")
  uv run -m http.server --directory {{output_dir}}

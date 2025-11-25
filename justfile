output_dir := '_site'

build: download unzip collect cleanup

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

cleanup:
  rm -rf core-products-icons category-icons *.zip

serve:
  python -m http.server --directory {{output_dir}} 

default: download unzip collect

download:
  curl \
    -O https://services.google.com/fh/files/misc/core-products-icons.zip \
    -O https://services.google.com/fh/files/misc/category-icons.zip

unzip:
  unzip -q -d core-products-icons core-products-icons.zip 
  unzip -q -d category-icons category-icons.zip 

collect:
  mkdir -p _site/core _site/category
  find core-products-icons -type f -regextype posix-extended -iregex ".*\.(png|svg)$" -exec mv -t _site/core {} +
  find category-icons -type f -regextype posix-extended -iregex ".*\.(png|svg)$" -exec mv -t _site/category {} +

cleanup:
  rm -rf core-products-icons category-icons *.zip

serve:
  python -m http.server --directory _site

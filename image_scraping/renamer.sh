for f in ./*/*/*; do 
    type=$( file "$f" | grep -oP '\w+(?= image data)' )
    case $type in  
        PNG)  newext=png ;; 
        JPEG) newext=jpg ;; 
        *)    echo "??? what is this: $f"; continue ;; 
    esac
    ext=`basename f`   # remove everything up to and including the last dot
    
        # remove "echo" if you're satisfied it's working
    mv "$f" "$f.$newext"
    
done

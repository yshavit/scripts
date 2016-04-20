import System.IO(getContents, putStr)

main :: IO ()
main = do stdin <- getContents
          putStr (trimR stdin)

trimR :: String -> String
trimR ""    = ""
trimR "\n"  = ""
trimR (h:t) = h : trimR t

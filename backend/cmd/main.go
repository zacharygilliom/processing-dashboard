package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/rocketlaunchr/dataframe-go/imports"
)

func main() {
	// Read in our CSV file
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	csv_file, err := os.Open("../data/Master Submitted Log.csv")
	df, err := imports.LoadFromCSV(ctx, csv_file)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(df)

}

function decript(text){
    while(text.includes("Ã¤")){
        text = text.replace("Ã¤","ä");
    }
    while(text.includes("Ã¼")){
        text = text.replace("Ã¼","ü");
    }
    return(text);
}
package com.example.demo.Controller;


import com.example.demo.Model.Model;
import org.python.apache.commons.compress.utils.FileNameUtils;
import org.python.util.PythonInterpreter;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;


import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@CrossOrigin(value = "http://localhost:3000")
@RestController
public class Controller {

    public static String s;

    public static String imageDirectory = System.getProperty("user.dir") + "/images/";

    @PostMapping(value="", produces = {MediaType.IMAGE_PNG_VALUE, "application/json"})
    public void run(@RequestParam("file") MultipartFile file) throws IOException {
        // make directory
        File directory = new File(imageDirectory);
        if(!directory.exists()){
            directory.mkdir();
        }

        Path fileNamePath = Paths.get(imageDirectory,
                "image".concat(".").concat(FileNameUtils.getExtension(file.getOriginalFilename())));


        Files.write(fileNamePath, file.getBytes());


        ProcessBuilder builder = new ProcessBuilder("python", System.getProperty("user.dir") + "\\src\\main\\java\\com\\example\\demo\\Controller\\grade_krutik.py");
        Process process = builder.start();

        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        BufferedReader readers = new BufferedReader(new InputStreamReader(process.getErrorStream()));

        String lines = null;
        while((lines = reader.readLine())!=null){
            System.out.println("lines "+ lines);
        }

        while((lines = readers.readLine())!=null){
            System.out.println("lines "+ lines);
        }
//        String command = "python /c D:\\IUB course\\temp\\spring-python\\demo\\src\\main\\java\\com\\example\\demo\\Controller\\grade_krutik.py";
//        Process p = Runtime.getRuntime().exec(command);
    }
}

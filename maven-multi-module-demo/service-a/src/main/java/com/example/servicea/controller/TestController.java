package com.example.servicea.controller;

import com.example.common.CommonUtil;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * 测试控制器 - 演示使用common模块的工具类
 */
@RestController
@RequestMapping("/api")
public class TestController {

    @GetMapping("/hello")
    public String hello() {
        // 使用common模块的工具类
        return CommonUtil.getMessage();
    }

    @GetMapping("/format")
    public String format(@RequestParam(defaultValue = "hello world") String message) {
        // 使用common模块的工具类
        return CommonUtil.formatMessage(message);
    }
}

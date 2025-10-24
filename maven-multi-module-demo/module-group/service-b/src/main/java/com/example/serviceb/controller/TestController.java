package com.example.serviceb.controller;

import com.example.common.CommonUtil;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * 测试控制器 - 演示嵌套子模块也可以使用common模块的工具类
 */
@RestController
@RequestMapping("/api")
public class TestController {

    @GetMapping("/hello")
    public String hello() {
        // 使用common模块的工具类
        return "Service B: " + CommonUtil.getMessage();
    }

    @GetMapping("/format")
    public String format(@RequestParam(defaultValue = "nested module") String message) {
        // 使用common模块的工具类
        return "Service B formatted: " + CommonUtil.formatMessage(message);
    }
}

$Host.UI.RawUI.WindowTitle = 'IALD - Kimi Pro - mesma conta Google do aplicativo'
Write-Host 'Entre usando a MESMA conta Google que mostra o plano Pro no aplicativo Kimi.'
Write-Host 'Se o navegador entrar automaticamente em outra conta, troque a conta na pagina do Kimi.'
& 'C:\Python314\python.exe' -X utf8 'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\login_provider.py' kimi
